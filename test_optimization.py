"""
Test optimized system vs original
Compare accuracy improvements
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity
import time


class QueryExpander:
    """Expand queries for better retrieval"""
    
    @staticmethod
    def expand_query(query: str) -> list:
        """Generate query variations"""
        variations = [query]
        
        synonyms = {
            'رخصة': ['ترخيص', 'تصريح'],
            'ترخيص': ['رخصة', 'تصريح'],
            'تصريح': ['رخصة', 'ترخيص'],
            'طلب': ['تقديم'],
            'كيف': ['ما هي خطوات'],
            'أحصل': ['احصل', 'استخرج'],
        }
        
        for word, syns in synonyms.items():
            if word in query:
                for syn in syns[:1]:  # Only 1 synonym
                    variations.append(query.replace(word, syn))
        
        return list(set(variations))[:2]  # Max 2 variations


def test_system(embeddings_path, chunks_path, meta_path, use_expansion=False):
    """Test a retrieval system"""
    
    # Load
    embeddings = np.load(embeddings_path).astype('float32')
    faiss.normalize_L2(embeddings)
    
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Load model
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    # Load test queries
    with open('experiments/test_queries_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    test_queries = dataset['queries'][:50]
    
    # Test
    expander = QueryExpander()
    correct = 0
    total = len(test_queries)
    
    for test_query in test_queries:
        query = test_query['query_ar']
        expected = test_query['category']
        
        if use_expansion:
            # Query expansion
            variations = expander.expand_query(query)
            query_embs = model.encode(variations)
            query_emb = np.mean(query_embs, axis=0).astype('float32').reshape(1, -1)
        else:
            # Single query
            query_emb = model.encode([query])[0].astype('float32').reshape(1, -1)
        
        faiss.normalize_L2(query_emb)
        
        # Search
        similarities = cosine_similarity(query_emb, embeddings)[0]
        top_idx = np.argmax(similarities)
        
        top_category = metadata[top_idx]['category']
        
        if top_category == expected:
            correct += 1
    
    accuracy = correct / total
    return accuracy, correct, total


def main():
    """Compare systems"""
    
    print("="*80)
    print("OPTIMIZATION COMPARISON")
    print("="*80)
    
    print("\n1. Testing ORIGINAL system...")
    acc1, c1, t1 = test_system(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json',
        use_expansion=False
    )
    print(f"   Accuracy: {acc1:.1%} ({c1}/{t1})")
    
    print("\n2. Testing OPTIMIZED system (no expansion)...")
    acc2, c2, t2 = test_system(
        'index/embeddings_optimized.npy',
        'index/corpus_chunks_optimized.json',
        'index/corpus_meta_optimized.json',
        use_expansion=False
    )
    print(f"   Accuracy: {acc2:.1%} ({c2}/{t2})")
    
    print("\n3. Testing OPTIMIZED system (with query expansion)...")
    acc3, c3, t3 = test_system(
        'index/embeddings_optimized.npy',
        'index/corpus_chunks_optimized.json',
        'index/corpus_meta_optimized.json',
        use_expansion=True
    )
    print(f"   Accuracy: {acc3:.1%} ({c3}/{t3})")
    
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    
    print(f"\nOriginal System:           {acc1:.1%}")
    print(f"Optimized (no expansion):  {acc2:.1%}  ({acc2-acc1:+.1%})")
    print(f"Optimized (with expansion): {acc3:.1%}  ({acc3-acc1:+.1%})")
    
    if acc3 > acc1:
        print(f"\n[SUCCESS] Improvement: {acc3-acc1:.1%} ({c3-c1} more correct)")
    else:
        print(f"\n[WARNING] No improvement")
    
    return {
        'original': acc1,
        'optimized': acc2,
        'optimized_expanded': acc3
    }


if __name__ == "__main__":
    results = main()
