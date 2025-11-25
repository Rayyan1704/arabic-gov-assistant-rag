"""
Test script for Day 5: Category-specific retrieval and reranking.
Compares three approaches:
1. Global search (baseline)
2. Category-specific search
3. Reranked search
"""

from src.category_retrieval import CategoryRetriever, RerankedRetriever
from sentence_transformers import SentenceTransformer
import json


def main():
    print("="*80)
    print("DAY 5: CATEGORY RETRIEVAL + RERANKING TEST")
    print("="*80)
    
    # Load model
    print("\nLoading embedding model...")
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    print("✅ Model loaded")
    
    # Initialize retrievers
    print("\n" + "="*80)
    print("INITIALIZING RETRIEVERS")
    print("="*80)
    
    print("\n1. Basic Category Retriever:")
    basic_retriever = CategoryRetriever(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json'
    )
    
    print("\n2. Reranked Retriever:")
    reranked_retriever = RerankedRetriever(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json'
    )
    
    # Test queries (diverse categories)
    test_queries = [
        {
            'query': 'كيف أحصل على بطاقة صحية في قطر؟',
            'expected_category': 'health'
        },
        {
            'query': 'ما هي إجراءات فتح شركة جديدة؟',
            'expected_category': 'business'
        },
        {
            'query': 'كيف أسجل أطفالي في المدرسة؟',
            'expected_category': 'education'
        },
        {
            'query': 'ما هي متطلبات الحصول على رخصة قيادة؟',
            'expected_category': 'transportation'
        },
        {
            'query': 'كيف أستأجر شقة في الدوحة؟',
            'expected_category': 'housing'
        }
    ]
    
    results_summary = []
    
    # Test each query
    for i, test in enumerate(test_queries, 1):
        query = test['query']
        expected_cat = test['expected_category']
        
        print("\n" + "="*80)
        print(f"TEST {i}/5")
        print("="*80)
        print(f"Query: {query}")
        print(f"Expected category: {expected_cat}")
        
        # Detect category
        detected_cat = basic_retriever.detect_category(query)
        print(f"Detected category: {detected_cat}")
        category_correct = detected_cat == expected_cat
        print(f"Category detection: {'✅ CORRECT' if category_correct else '❌ WRONG'}")
        
        # Get query embedding
        query_emb = model.encode([query])[0]
        
        # Approach 1: Global search
        print("\n--- APPROACH 1: GLOBAL SEARCH ---")
        global_results = basic_retriever.search(query_emb, category=None, k=5)
        for r in global_results[:3]:
            print(f"  [{r['rank']}] Score: {r['score']:.3f} | Category: {r['metadata']['category']}")
            print(f"      {r['chunk'][:80]}...")
        
        # Approach 2: Category-specific search
        print("\n--- APPROACH 2: CATEGORY-SPECIFIC SEARCH ---")
        if detected_cat:
            cat_results = basic_retriever.search(query_emb, category=detected_cat, k=5)
            for r in cat_results[:3]:
                print(f"  [{r['rank']}] Score: {r['score']:.3f} | Category: {r['metadata']['category']}")
                print(f"      {r['chunk'][:80]}...")
        else:
            print("  No category detected, using global search")
            cat_results = global_results
        
        # Approach 3: Reranked search
        print("\n--- APPROACH 3: RERANKED SEARCH ---")
        reranked_results = reranked_retriever.search_with_rerank(
            query, query_emb, category=detected_cat, initial_k=20, final_k=5
        )
        for r in reranked_results[:3]:
            print(f"  [{r['rank']}] Rerank: {r['rerank_score']:.3f} | Original: {r['original_score']:.3f} | Category: {r['metadata']['category']}")
            print(f"      {r['chunk'][:80]}...")
        
        # Store results for summary
        results_summary.append({
            'query': query,
            'expected_category': expected_cat,
            'detected_category': detected_cat,
            'category_correct': category_correct,
            'global_top1_score': global_results[0]['score'],
            'category_top1_score': cat_results[0]['score'],
            'reranked_top1_score': reranked_results[0]['rerank_score'],
            'global_top1_category': global_results[0]['metadata']['category'],
            'reranked_top1_category': reranked_results[0]['metadata']['category']
        })
    
    # Final summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    category_accuracy = sum(1 for r in results_summary if r['category_correct']) / len(results_summary)
    print(f"\nCategory Detection Accuracy: {category_accuracy*100:.1f}% ({sum(1 for r in results_summary if r['category_correct'])}/{len(results_summary)})")
    
    print("\nAverage Top-1 Scores:")
    avg_global = sum(r['global_top1_score'] for r in results_summary) / len(results_summary)
    avg_category = sum(r['category_top1_score'] for r in results_summary) / len(results_summary)
    avg_reranked = sum(r['reranked_top1_score'] for r in results_summary) / len(results_summary)
    
    print(f"  Global search:    {avg_global:.3f}")
    print(f"  Category search:  {avg_category:.3f}")
    print(f"  Reranked search:  {avg_reranked:.3f}")
    
    # Check if reranking changed order
    rerank_changes = sum(1 for r in results_summary 
                        if r['global_top1_category'] != r['reranked_top1_category'])
    print(f"\nReranking changed top-1 result: {rerank_changes}/{len(results_summary)} times")
    
    # Save results
    output_file = 'index/category_reranking_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_summary, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Results saved to {output_file}")
    
    print("\n" + "="*80)
    print("CONCLUSIONS")
    print("="*80)
    print("\n1. Category Detection:")
    if category_accuracy >= 0.8:
        print("   ✅ Good - keyword-based detection works well")
    else:
        print("   ⚠️  Could be improved with ML-based classification")
    
    print("\n2. Category-Specific Search:")
    if avg_category > avg_global:
        print("   ✅ Better than global search - reduces search space effectively")
    else:
        print("   ⚠️  Similar to global search - may not be needed for small corpus")
    
    print("\n3. Reranking:")
    if avg_reranked > avg_global * 1.05:
        print("   ✅ Significant improvement - cross-encoder adds value")
    elif rerank_changes > 0:
        print("   ⚠️  Changes results but unclear if better - needs human evaluation")
    else:
        print("   ⚠️  Minimal impact - embedding search already good enough")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
