"""
Analyze which queries are failing and why
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity


def analyze_failures():
    """Find and analyze failing queries"""
    
    print("="*80)
    print("FAILURE ANALYSIS")
    print("="*80)
    
    # Load system
    embeddings = np.load('index/embeddings.npy').astype('float32')
    faiss.normalize_L2(embeddings)
    
    with open('index/corpus_chunks.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    with open('index/corpus_meta.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    # Load test queries
    with open('experiments/test_queries_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    test_queries = dataset['queries'][:50]
    
    # Analyze
    failures = []
    successes = []
    
    for test_query in test_queries:
        query = test_query['query_ar']
        expected = test_query['category']
        
        query_emb = model.encode([query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        
        sims = cosine_similarity(query_emb, embeddings)[0]
        top_indices = np.argsort(sims)[-5:][::-1]
        
        top_cat = metadata[top_indices[0]]['category']
        top_score = sims[top_indices[0]]
        
        result = {
            'query': query,
            'expected': expected,
            'predicted': top_cat,
            'score': float(top_score),
            'top5_categories': [metadata[idx]['category'] for idx in top_indices],
            'top5_scores': [float(sims[idx]) for idx in top_indices],
            'top_chunk': chunks[top_indices[0]][:200]
        }
        
        if top_cat == expected:
            successes.append(result)
        else:
            failures.append(result)
    
    # Report
    print(f"\nTotal: {len(test_queries)}")
    print(f"Success: {len(successes)} ({len(successes)/len(test_queries):.1%})")
    print(f"Failures: {len(failures)} ({len(failures)/len(test_queries):.1%})")
    
    print("\n" + "="*80)
    print("FAILURE CASES")
    print("="*80)
    
    for i, fail in enumerate(failures, 1):
        print(f"\n[{i}] Query: {fail['query']}")
        print(f"    Expected: {fail['expected']}")
        print(f"    Predicted: {fail['predicted']} (score: {fail['score']:.3f})")
        print(f"    Top 5: {fail['top5_categories']}")
        print(f"    Chunk preview: {fail['top_chunk'][:100]}...")
        
        # Check if expected category is in top 5
        if fail['expected'] in fail['top5_categories']:
            rank = fail['top5_categories'].index(fail['expected']) + 1
            print(f"    [NOTE] Correct category is at rank {rank}")
    
    # Analyze patterns
    print("\n" + "="*80)
    print("FAILURE PATTERNS")
    print("="*80)
    
    from collections import Counter
    
    expected_cats = Counter(f['expected'] for f in failures)
    predicted_cats = Counter(f['predicted'] for f in failures)
    
    print("\nMost confused categories (expected):")
    for cat, count in expected_cats.most_common(5):
        print(f"  {cat}: {count} failures")
    
    print("\nMost common wrong predictions:")
    for cat, count in predicted_cats.most_common(5):
        print(f"  {cat}: {count} times")
    
    # Score analysis
    fail_scores = [f['score'] for f in failures]
    success_scores = [s['score'] for s in successes]
    
    print(f"\nAverage scores:")
    print(f"  Failures: {np.mean(fail_scores):.3f}")
    print(f"  Successes: {np.mean(success_scores):.3f}")
    print(f"  Difference: {np.mean(success_scores) - np.mean(fail_scores):.3f}")
    
    # Save detailed report
    report = {
        'summary': {
            'total': len(test_queries),
            'successes': len(successes),
            'failures': len(failures),
            'accuracy': len(successes) / len(test_queries)
        },
        'failures': failures,
        'patterns': {
            'expected_categories': dict(expected_cats),
            'predicted_categories': dict(predicted_cats)
        }
    }
    
    with open('index/failure_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Detailed report saved to index/failure_analysis.json")
    
    return report


if __name__ == "__main__":
    report = analyze_failures()
