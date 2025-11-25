"""
Experiment 2: Hybrid Retrieval System
Combines semantic search (embeddings) with keyword search (BM25).

Research Question: Does hybrid retrieval improve accuracy over semantic-only?
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import faiss
from sklearn.metrics.pairwise import cosine_similarity
import time
from typing import List, Dict


class HybridRetriever:
    """Hybrid retrieval combining semantic search and BM25."""
    
    def __init__(self, embeddings_path, chunks_path, metadata_path):
        print("="*80)
        print("EXPERIMENT 2: HYBRID RETRIEVAL")
        print("="*80)
        
        print("\nLoading data...")
        if not os.path.isabs(embeddings_path):
            base_dir = os.path.join(os.path.dirname(__file__), '..')
            embeddings_path = os.path.join(base_dir, embeddings_path)
            chunks_path = os.path.join(base_dir, chunks_path)
            metadata_path = os.path.join(base_dir, metadata_path)
        
        self.embeddings = np.load(embeddings_path).astype('float32')
        
        with open(chunks_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        print(f"[OK] Loaded {len(self.chunks)} chunks")
        
        faiss.normalize_L2(self.embeddings)
        
        print("Loading embedding model...")
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        print("Building BM25 index...")
        self._build_bm25_index()
        
        print("[OK] Setup complete\n")
    
    def _build_bm25_index(self):
        """Build BM25 index from chunks"""
        tokenized_chunks = [chunk.split() for chunk in self.chunks]
        self.bm25 = BM25Okapi(tokenized_chunks)
        print(f"[OK] BM25 index built with {len(tokenized_chunks)} documents")
    
    def semantic_search(self, query: str, k: int = 10):
        """Pure semantic search using embeddings"""
        start = time.time()
        
        query_emb = self.model.encode([query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        
        similarities = cosine_similarity(query_emb, self.embeddings)[0]
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        elapsed = time.time() - start
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            results.append({
                'rank': rank,
                'index': int(idx),
                'score': float(similarities[idx]),
                'category': self.metadata[idx]['category'],
                'chunk': self.chunks[idx]
            })
        
        return results, elapsed
    
    def bm25_search(self, query: str, k: int = 10):
        """Pure BM25 keyword search"""
        start = time.time()
        
        query_tokens = query.split()
        scores = self.bm25.get_scores(query_tokens)
        top_indices = np.argsort(scores)[-k:][::-1]
        
        elapsed = time.time() - start
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            results.append({
                'rank': rank,
                'index': int(idx),
                'score': float(scores[idx]),
                'category': self.metadata[idx]['category'],
                'chunk': self.chunks[idx]
            })
        
        return results, elapsed
    
    def hybrid_search_weighted(self, query: str, k: int = 10, semantic_weight: float = 0.7):
        """Hybrid search with weighted combination."""
        start = time.time()
        
        bm25_weight = 1.0 - semantic_weight
        
        query_emb = self.model.encode([query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        semantic_scores = cosine_similarity(query_emb, self.embeddings)[0]
        
        if semantic_scores.max() > semantic_scores.min():
            semantic_scores = (semantic_scores - semantic_scores.min()) / (semantic_scores.max() - semantic_scores.min())
        
        query_tokens = query.split()
        bm25_scores = self.bm25.get_scores(query_tokens)
        
        if bm25_scores.max() > bm25_scores.min():
            bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min())
        
        combined_scores = (semantic_weight * semantic_scores) + (bm25_weight * bm25_scores)
        top_indices = np.argsort(combined_scores)[-k:][::-1]
        
        elapsed = time.time() - start
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            results.append({
                'rank': rank,
                'index': int(idx),
                'score': float(combined_scores[idx]),
                'semantic_score': float(semantic_scores[idx]),
                'bm25_score': float(bm25_scores[idx]),
                'category': self.metadata[idx]['category'],
                'chunk': self.chunks[idx]
            })
        
        return results, elapsed
    
    def hybrid_search_cascade(self, query: str, k: int = 10, first_stage_k: int = 50):
        """Cascade hybrid: BM25 first stage, semantic reranking."""
        start = time.time()
        
        query_tokens = query.split()
        bm25_scores = self.bm25.get_scores(query_tokens)
        top_indices = np.argsort(bm25_scores)[-first_stage_k:][::-1]
        
        query_emb = self.model.encode([query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        
        candidate_embeddings = self.embeddings[top_indices]
        semantic_scores = cosine_similarity(query_emb, candidate_embeddings)[0]
        
        reranked_indices = np.argsort(semantic_scores)[-k:][::-1]
        final_indices = top_indices[reranked_indices]
        
        elapsed = time.time() - start
        
        results = []
        for rank, idx in enumerate(final_indices, 1):
            results.append({
                'rank': rank,
                'index': int(idx),
                'score': float(semantic_scores[reranked_indices[rank-1]]),
                'bm25_score': float(bm25_scores[idx]),
                'category': self.metadata[idx]['category'],
                'chunk': self.chunks[idx]
            })
        
        return results, elapsed
    
    def evaluate_method(self, query: str, expected_category: str, method: str, **kwargs):
        """Evaluate a single method on a query"""
        
        if method == 'semantic':
            results, elapsed = self.semantic_search(query, k=10)
        elif method == 'bm25':
            results, elapsed = self.bm25_search(query, k=10)
        elif method == 'hybrid_weighted':
            results, elapsed = self.hybrid_search_weighted(query, k=10, **kwargs)
        elif method == 'hybrid_cascade':
            results, elapsed = self.hybrid_search_cascade(query, k=10, **kwargs)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        top_category = results[0]['category']
        p_at_1 = 1 if top_category == expected_category else 0
        
        top3_categories = [r['category'] for r in results[:3]]
        p_at_3 = 1 if expected_category in top3_categories else 0
        
        top5_categories = [r['category'] for r in results[:5]]
        p_at_5 = 1 if expected_category in top5_categories else 0
        
        try:
            rank = [r['category'] for r in results].index(expected_category) + 1
            mrr = 1.0 / rank
        except ValueError:
            mrr = 0.0
        
        return {
            'method': method,
            'query': query,
            'expected': expected_category,
            'top_category': top_category,
            'p@1': p_at_1,
            'p@3': p_at_3,
            'p@5': p_at_5,
            'mrr': mrr,
            'time': elapsed,
            'top_results': results[:5]
        }


def run_experiment():
    """Run complete hybrid retrieval experiment"""
    
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    retriever = HybridRetriever(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json'
    )
    
    print("\n" + "="*80)
    print("LOADING TEST QUERIES")
    print("="*80)
    
    queries_path = os.path.join(os.path.dirname(__file__), 'test_queries_dataset.json')
    with open(queries_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    test_queries = dataset['queries'][:50]
    print(f"[OK] Loaded {len(test_queries)} test queries")
    
    methods = [
        {'name': 'semantic', 'params': {}},
        {'name': 'bm25', 'params': {}},
        {'name': 'hybrid_weighted', 'params': {'semantic_weight': 0.7}},
        {'name': 'hybrid_weighted', 'params': {'semantic_weight': 0.5}},
        {'name': 'hybrid_cascade', 'params': {'first_stage_k': 50}}
    ]
    
    print("\n" + "="*80)
    print("RUNNING EXPERIMENTS")
    print("="*80)
    
    all_results = {method['name'] + '_' + str(method['params']): [] for method in methods}
    
    for i, test_query in enumerate(test_queries, 1):
        query = test_query['query_ar']
        expected = test_query['category']
        
        print(f"\n[{i}/{len(test_queries)}] {query[:50]}...")
        
        for method in methods:
            method_key = method['name'] + '_' + str(method['params'])
            result = retriever.evaluate_method(
                query, expected, 
                method['name'], 
                **method['params']
            )
            all_results[method_key].append(result)
    
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    
    summary = {}
    for method_key, results in all_results.items():
        summary[method_key] = {
            'P@1': np.mean([r['p@1'] for r in results]),
            'P@3': np.mean([r['p@3'] for r in results]),
            'P@5': np.mean([r['p@5'] for r in results]),
            'MRR': np.mean([r['mrr'] for r in results]),
            'Avg_Time': np.mean([r['time'] for r in results]),
            'Total_Correct': sum([r['p@1'] for r in results])
        }
    
    print("\n{:<35} {:>8} {:>8} {:>8} {:>8} {:>10}".format(
        "Method", "P@1", "P@3", "P@5", "MRR", "Time(s)"
    ))
    print("-"*80)
    
    for method_key, metrics in summary.items():
        print("{:<35} {:>7.1%} {:>7.1%} {:>7.1%} {:>8.3f} {:>10.4f}".format(
            method_key[:35],
            metrics['P@1'],
            metrics['P@3'],
            metrics['P@5'],
            metrics['MRR'],
            metrics['Avg_Time']
        ))
    
    output = {
        'experiment': 'hybrid_retrieval',
        'test_queries': len(test_queries),
        'methods_tested': len(methods),
        'summary': summary,
        'detailed_results': all_results
    }
    
    output_path = os.path.join(base_dir, 'index', 'experiment2_hybrid_retrieval.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("\n[OK] Results saved to experiment2_hybrid_retrieval.json")
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    
    best_method = max(summary.items(), key=lambda x: x[1]['P@1'])
    print(f"\nBest Method: {best_method[0]}")
    print(f"P@1: {best_method[1]['P@1']:.1%}")
    print(f"P@3: {best_method[1]['P@3']:.1%}")
    print(f"P@5: {best_method[1]['P@5']:.1%}")
    print(f"MRR: {best_method[1]['MRR']:.3f}")
    print(f"Avg Time: {best_method[1]['Avg_Time']:.4f}s")
    
    print("\n[OK] Experiment 2 complete!")


if __name__ == "__main__":
    run_experiment()
