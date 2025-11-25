"""
Comprehensive Accuracy Test
Tests 20 critical queries for 95%+ accuracy
"""

import sys
sys.path.append('src')

from sentence_transformers import SentenceTransformer
from category_retrieval import RerankedRetriever
import json


def main():
    print("="*80)
    print("                    COMPREHENSIVE ACCURACY TEST")
    print("="*80)
    
    # Load components
    print("\nLoading models...")
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    retriever = RerankedRetriever(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json'
    )
    print("✅ Models loaded")
    
    # Test queries with expected categories
    test_queries = [
        # Transportation (5)
        {'query': 'كيف أحصل على رخصة ليموزين؟', 'expected': 'transportation'},
        {'query': 'How do I get a limousine license?', 'expected': 'transportation'},
        {'query': 'ما هي خطوات تأجير السيارات؟', 'expected': 'transportation'},
        {'query': 'Fish transport permit', 'expected': 'transportation'},
        {'query': 'Air cargo license', 'expected': 'transportation'},
        
        # Education (5)
        {'query': 'كيف أسجل في مقررات جامعة قطر؟', 'expected': 'education'},
        {'query': 'How to register for courses at Qatar University?', 'expected': 'education'},
        {'query': 'طلب كشف الدرجات', 'expected': 'education'},
        {'query': 'HBKU admission', 'expected': 'education'},
        {'query': 'Withdrawal from university', 'expected': 'education'},
        
        # Health (5)
        {'query': 'كيف أطلب استشارة طبية؟', 'expected': 'health'},
        {'query': 'How to request medical consultation?', 'expected': 'health'},
        {'query': 'تقرير طبي من حمد', 'expected': 'health'},
        {'query': 'Hamad Medical Corporation job', 'expected': 'health'},
        {'query': 'Healthcare practitioner license', 'expected': 'health'},
        
        # Business (5)
        {'query': 'كيف أقدم عروض المناقصات؟', 'expected': 'business'},
        {'query': 'How to submit tenders?', 'expected': 'business'},
        {'query': 'شهادة تأكيد استلام الطلب', 'expected': 'business'},
        {'query': 'Tax registration', 'expected': 'business'},
        {'query': 'Company financing', 'expected': 'business'},
    ]
    
    print(f"\nTesting {len(test_queries)} queries...")
    print("="*80)
    
    # Run tests
    correct_category = 0
    correct_retrieval = 0
    results = []
    
    for i, test in enumerate(test_queries, 1):
        query = test['query']
        expected = test['expected']
        
        # Category detection
        detected = retriever.detect_category(query)
        cat_match = (detected == expected)
        if cat_match:
            correct_category += 1
        
        # Retrieval
        query_emb = model.encode([query])[0]
        search_results = retriever.search_with_rerank(
            query, query_emb,
            category=detected,
            final_k=5
        )
        
        top_category = search_results[0]['metadata']['category']
        ret_match = (top_category == expected)
        if ret_match:
            correct_retrieval += 1
        
        status = "✅" if (cat_match and ret_match) else "❌"
        detected_str = detected if detected else "None"
        
        print(f"{status} [{i:2d}] {query[:50]:<50} → {detected_str:<15} (expected: {expected})")
        
        results.append({
            'query': query,
            'expected': expected,
            'detected': detected,
            'top_result': top_category,
            'category_correct': cat_match,
            'retrieval_correct': ret_match
        })
    
    # Summary
    print("="*80)
    print(f"Category Detection: {correct_category}/{len(test_queries)} ({100*correct_category/len(test_queries):.1f}%)")
    print(f"Retrieval Accuracy: {correct_retrieval}/{len(test_queries)} ({100*correct_retrieval/len(test_queries):.1f}%)")
    
    if correct_retrieval == len(test_queries):
        print("STATUS: ✅ PERFECT - 100% ACCURACY")
    elif correct_retrieval >= 19:
        print("STATUS: ✅ EXCELLENT - 95%+ ACCURACY")
    elif correct_retrieval >= 17:
        print("STATUS: ✅ GOOD - 85%+ ACCURACY")
    else:
        print("STATUS: ⚠️  NEEDS IMPROVEMENT")
    
    # Save results
    with open('index/accuracy_test_results.json', 'w') as f:
        json.dump({
            'total_queries': len(test_queries),
            'category_accuracy': correct_category / len(test_queries),
            'retrieval_accuracy': correct_retrieval / len(test_queries),
            'detailed_results': results
        }, f, indent=2)
    
    print("\n✅ Results saved to accuracy_test_results.json")


if __name__ == "__main__":
    main()
