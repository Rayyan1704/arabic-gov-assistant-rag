"""
Test with real-world unstructured queries
Like actual users would type
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity
from translator import TranslationService


def test_real_queries():
    """Test with messy real-world queries"""
    
    print("="*80)
    print("REAL-WORLD QUERY TEST")
    print("="*80)
    
    # Load system
    embeddings = np.load('index/embeddings.npy').astype('float32')
    faiss.normalize_L2(embeddings)
    
    with open('index/corpus_chunks.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    with open('index/corpus_meta.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    translator = TranslationService()
    
    # Real-world messy queries
    test_cases = [
        # English queries
        {
            'query': 'apply nurse qatar',
            'expected_category': 'health',
            'description': 'Short English - nurse application'
        },
        {
            'query': 'how to get limousine license',
            'expected_category': 'transportation',
            'description': 'English - limousine license'
        },
        {
            'query': 'register my kid school',
            'expected_category': 'education',
            'description': 'Broken English - school registration'
        },
        {
            'query': 'doctor search qatar',
            'expected_category': 'health',
            'description': 'Short English - find doctor'
        },
        {
            'query': 'business license renew',
            'expected_category': 'business',
            'description': 'English - business license'
        },
        
        # Arabic queries - informal/messy
        {
            'query': 'ابي رخصة سواقة',
            'expected_category': 'transportation',
            'description': 'Informal Arabic - driving license'
        },
        {
            'query': 'وين اسجل ولدي مدرسة',
            'expected_category': 'education',
            'description': 'Dialect Arabic - school registration'
        },
        {
            'query': 'شلون اطلع رخصة تجارية',
            'expected_category': 'business',
            'description': 'Gulf dialect - business license'
        },
        {
            'query': 'دكتور',
            'expected_category': 'health',
            'description': 'Single word - doctor'
        },
        {
            'query': 'مستشفى حمد',
            'expected_category': 'health',
            'description': 'Hospital name'
        },
        
        # Mixed/Typos
        {
            'query': 'limozin lisence',
            'expected_category': 'transportation',
            'description': 'Typos - limousine license'
        },
        {
            'query': 'تسجيل univercity',
            'expected_category': 'education',
            'description': 'Mixed Arabic/English with typo'
        },
        {
            'query': 'rent allowance',
            'expected_category': 'housing',
            'description': 'English - rent allowance'
        },
        {
            'query': 'court case',
            'expected_category': 'justice',
            'description': 'English - court/justice'
        },
        {
            'query': 'radio license',
            'expected_category': 'culture',
            'description': 'English - radio license'
        },
    ]
    
    print("\nTesting real-world queries...\n")
    
    results = []
    correct = 0
    
    for i, test in enumerate(test_cases, 1):
        query = test['query']
        expected = test['expected_category']
        desc = test['description']
        
        # Detect language and translate if needed
        is_english = any(c.isascii() and c.isalpha() for c in query)
        
        if is_english:
            # Translate to Arabic
            arabic_query = translator.translate_to_arabic(query)
            query_to_search = arabic_query
            lang = "EN"
        else:
            query_to_search = query
            lang = "AR"
        
        # Search
        query_emb = model.encode([query_to_search])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        
        sims = cosine_similarity(query_emb, embeddings)[0]
        top_idx = np.argmax(sims)
        top_cat = metadata[top_idx]['category']
        top_score = sims[top_idx]
        
        # Get top 3 for context
        top3_indices = np.argsort(sims)[-3:][::-1]
        top3_cats = [metadata[idx]['category'] for idx in top3_indices]
        
        is_correct = top_cat == expected
        if is_correct:
            correct += 1
            status = "✓"
        else:
            status = "✗"
        
        results.append({
            'query': query,
            'lang': lang,
            'expected': expected,
            'predicted': top_cat,
            'score': float(top_score),
            'top3': top3_cats,
            'correct': is_correct
        })
        
        print(f"[{i:2d}] {status} {lang} | {query:30s}")
        print(f"     {desc:40s}")
        print(f"     Expected: {expected:15s} Got: {top_cat:15s} (score: {top_score:.3f})")
        if not is_correct:
            print(f"     Top 3: {top3_cats}")
        print()
    
    # Summary
    accuracy = correct / len(test_cases)
    
    print("="*80)
    print("RESULTS")
    print("="*80)
    print(f"\nAccuracy: {accuracy:.1%} ({correct}/{len(test_cases)})")
    
    # By language
    en_results = [r for r in results if r['lang'] == 'EN']
    ar_results = [r for r in results if r['lang'] == 'AR']
    
    en_correct = sum(1 for r in en_results if r['correct'])
    ar_correct = sum(1 for r in ar_results if r['correct'])
    
    print(f"\nEnglish queries: {en_correct}/{len(en_results)} ({en_correct/len(en_results):.1%})")
    print(f"Arabic queries:  {ar_correct}/{len(ar_results)} ({ar_correct/len(ar_results):.1%})")
    
    # Failures
    failures = [r for r in results if not r['correct']]
    if failures:
        print(f"\nFailed queries ({len(failures)}):")
        for fail in failures:
            print(f"  - '{fail['query']}' → Expected: {fail['expected']}, Got: {fail['predicted']}")
    
    # Save report
    report = {
        'total': len(test_cases),
        'correct': correct,
        'accuracy': accuracy,
        'by_language': {
            'english': {'correct': en_correct, 'total': len(en_results)},
            'arabic': {'correct': ar_correct, 'total': len(ar_results)}
        },
        'results': results
    }
    
    with open('index/real_world_test.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Report saved to index/real_world_test.json")
    
    if accuracy < 0.8:
        print("\n⚠️  WARNING: Real-world accuracy is below 80%!")
        print("   System needs improvement for production use.")
    elif accuracy >= 0.9:
        print("\n✓ EXCELLENT: System handles real-world queries well!")
    else:
        print("\n✓ GOOD: System is production-ready with room for improvement.")
    
    return report


if __name__ == "__main__":
    report = test_real_queries()
