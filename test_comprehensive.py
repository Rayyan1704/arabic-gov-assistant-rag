"""
Comprehensive Testing Suite - 95%+ Accuracy Target
Tests 40+ queries (20 Arabic + 20 English) with performance optimization
"""
import sys
sys.path.append('src')

import time
import numpy as np
from sentence_transformers import SentenceTransformer
from category_retrieval import RerankedRetriever
from sklearn.metrics.pairwise import cosine_similarity
import json

print("="*80)
print("COMPREHENSIVE TESTING SUITE")
print("Target: 95%+ Accuracy | Optimized Performance")
print("="*80)

# Load models
print("\n[1/5] Loading models...")
start_time = time.time()
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
retriever = RerankedRetriever(
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)
load_time = time.time() - start_time
print(f"✅ Models loaded in {load_time:.2f}s")

# Test queries - 20 Arabic + 20 English
test_queries = [
    # Transportation (10 queries - 5 Arabic + 5 English)
    {
        'query': 'كيف أحصل على رخصة ليموزين؟',
        'expected_category': 'transportation',
        'language': 'ar'
    },
    {
        'query': 'ما هي خطوات تأجير السيارات؟',
        'expected_category': 'transportation',
        'language': 'ar'
    },
    {
        'query': 'كيف أحصل على ترخيص نقل الأسماك؟',
        'expected_category': 'transportation',
        'language': 'ar'
    },
    {
        'query': 'ما هي إجراءات الحصول على رخصة شحن جوي؟',
        'expected_category': 'transportation',
        'language': 'ar'
    },
    {
        'query': 'كيف أطلب تعميم على مركبة؟',
        'expected_category': 'transportation',
        'language': 'ar'
    },
    {
        'query': 'How do I get a limousine license in Qatar?',
        'expected_category': 'transportation',
        'language': 'en'
    },
    {
        'query': 'What are the requirements for car rental license?',
        'expected_category': 'transportation',
        'language': 'en'
    },
    {
        'query': 'How to apply for air cargo license?',
        'expected_category': 'transportation',
        'language': 'en'
    },
    {
        'query': 'Fish transport permit application process',
        'expected_category': 'transportation',
        'language': 'en'
    },
    {
        'query': 'Vehicle circulation request procedure',
        'expected_category': 'transportation',
        'language': 'en'
    },
    
    # Education (10 queries - 5 Arabic + 5 English)
    {
        'query': 'كيف أسجل في مقررات جامعة قطر؟',
        'expected_category': 'education',
        'language': 'ar'
    },
    {
        'query': 'ما هي خطوات طلب كشف الدرجات؟',
        'expected_category': 'education',
        'language': 'ar'
    },
    {
        'query': 'كيف أتقدم للقبول في جامعة حمد بن خليفة؟',
        'expected_category': 'education',
        'language': 'ar'
    },
    {
        'query': 'كيف أنسحب من جامعة قطر؟',
        'expected_category': 'education',
        'language': 'ar'
    },
    {
        'query': 'أين أجد دليل المراكز البحثية في قطر؟',
        'expected_category': 'education',
        'language': 'ar'
    },
    {
        'query': 'How to register for courses at Qatar University?',
        'expected_category': 'education',
        'language': 'en'
    },
    {
        'query': 'Request transcript from Qatar University',
        'expected_category': 'education',
        'language': 'en'
    },
    {
        'query': 'HBKU admission application process',
        'expected_category': 'education',
        'language': 'en'
    },
    {
        'query': 'Withdraw from Qatar University procedure',
        'expected_category': 'education',
        'language': 'en'
    },
    {
        'query': 'Research centers guide in Qatar',
        'expected_category': 'education',
        'language': 'en'
    },
    
    # Health (10 queries - 5 Arabic + 5 English)
    {
        'query': 'كيف أطلب استشارة طبية؟',
        'expected_category': 'health',
        'language': 'ar'
    },
    {
        'query': 'كيف أحصل على تقرير طبي من حمد؟',
        'expected_category': 'health',
        'language': 'ar'
    },
    {
        'query': 'كيف أتواصل مع مؤسسة حمد للاستشارات العاجلة؟',
        'expected_category': 'health',
        'language': 'ar'
    },
    {
        'query': 'كيف أتقدم للتوظيف في مؤسسة حمد الطبية؟',
        'expected_category': 'health',
        'language': 'ar'
    },
    {
        'query': 'كيف أحصل على ترخيص ممارس صحي؟',
        'expected_category': 'health',
        'language': 'ar'
    },
    {
        'query': 'How to request medical consultation?',
        'expected_category': 'health',
        'language': 'en'
    },
    {
        'query': 'Get medical report from Hamad Medical',
        'expected_category': 'health',
        'language': 'en'
    },
    {
        'query': 'Urgent medical consultation at HMC',
        'expected_category': 'health',
        'language': 'en'
    },
    {
        'query': 'Job application at Hamad Medical Corporation',
        'expected_category': 'health',
        'language': 'en'
    },
    {
        'query': 'Healthcare practitioner license application',
        'expected_category': 'health',
        'language': 'en'
    },
    
    # Business (10 queries - 5 Arabic + 5 English)
    {
        'query': 'كيف أقدم عروض المناقصات؟',
        'expected_category': 'business',
        'language': 'ar'
    },
    {
        'query': 'كيف أحصل على شهادة تأكيد استلام الطلب؟',
        'expected_category': 'business',
        'language': 'ar'
    },
    {
        'query': 'كيف أسجل نفسي كمكلف في الضرائب؟',
        'expected_category': 'business',
        'language': 'ar'
    },
    {
        'query': 'كيف أعيد تفعيل رخصة تجارية؟',
        'expected_category': 'business',
        'language': 'ar'
    },
    {
        'query': 'كيف أحصل على تمويل من بنك قطر للتنمية؟',
        'expected_category': 'business',
        'language': 'ar'
    },
    {
        'query': 'How to submit tenders in Qatar?',
        'expected_category': 'business',
        'language': 'en'
    },
    {
        'query': 'CRA acknowledgement certificate request',
        'expected_category': 'business',
        'language': 'en'
    },
    {
        'query': 'Tax self-registration process',
        'expected_category': 'business',
        'language': 'en'
    },
    {
        'query': 'Reactivate commercial license',
        'expected_category': 'business',
        'language': 'en'
    },
    {
        'query': 'Company financing from Qatar Development Bank',
        'expected_category': 'business',
        'language': 'en'
    },
]

print(f"\n[2/5] Created test set: {len(test_queries)} queries")
print(f"  - Arabic: {sum(1 for q in test_queries if q['language'] == 'ar')}")
print(f"  - English: {sum(1 for q in test_queries if q['language'] == 'en')}")

# Test configurations
configs = [
    {'name': 'Basic (No optimization)', 'use_category': False, 'use_rerank': False},
    {'name': 'Category Detection', 'use_category': True, 'use_rerank': False},
    {'name': 'Full (Category + Rerank)', 'use_category': True, 'use_rerank': True},
]

results_summary = []

for config in configs:
    print(f"\n{'='*80}")
    print(f"Testing: {config['name']}")
    print('='*80)
    
    correct = 0
    total_time = 0
    details = []
    
    for test in test_queries:
        query = test['query']
        expected_cat = test['expected_category']
        
        # Measure time
        start = time.time()
        
        # Get embedding
        query_emb = model.encode([query])[0]
        
        # Detect category
        category = None
        if config['use_category']:
            category = retriever.detect_category(query)
        
        # Retrieve
        if config['use_rerank']:
            results = retriever.search_with_rerank(
                query, query_emb,
                category=category,
                initial_k=20,
                final_k=5
            )
        else:
            results = retriever.search(
                query_emb,
                category=category,
                k=5
            )
        
        elapsed = time.time() - start
        total_time += elapsed
        
        # Check if correct
        top_category = results[0]['metadata']['category']
        is_correct = (top_category == expected_cat)
        if is_correct:
            correct += 1
        
        details.append({
            'query': query,
            'language': test['language'],
            'expected': expected_cat,
            'got': top_category,
            'correct': is_correct,
            'time': elapsed,
            'score': results[0]['score']
        })
    
    # Calculate metrics
    accuracy = correct / len(test_queries)
    avg_time = total_time / len(test_queries)
    
    # Language-specific accuracy
    ar_correct = sum(1 for d in details if d['language'] == 'ar' and d['correct'])
    ar_total = sum(1 for d in details if d['language'] == 'ar')
    ar_accuracy = ar_correct / ar_total if ar_total > 0 else 0
    
    en_correct = sum(1 for d in details if d['language'] == 'en' and d['correct'])
    en_total = sum(1 for d in details if d['language'] == 'en')
    en_accuracy = en_correct / en_total if en_total > 0 else 0
    
    results_summary.append({
        'config': config['name'],
        'accuracy': accuracy,
        'ar_accuracy': ar_accuracy,
        'en_accuracy': en_accuracy,
        'avg_time': avg_time,
        'total_time': total_time,
        'correct': correct,
        'total': len(test_queries)
    })
    
    print(f"\nResults:")
    print(f"  Overall Accuracy: {accuracy:.1%} ({correct}/{len(test_queries)})")
    print(f"  Arabic Accuracy:  {ar_accuracy:.1%} ({ar_correct}/{ar_total})")
    print(f"  English Accuracy: {en_accuracy:.1%} ({en_correct}/{en_total})")
    print(f"  Avg Time: {avg_time*1000:.1f}ms")
    print(f"  Total Time: {total_time:.2f}s")

# Final comparison
print(f"\n{'='*80}")
print("FINAL COMPARISON")
print('='*80)

print(f"\n{'Configuration':<30} {'Accuracy':<12} {'AR Acc':<10} {'EN Acc':<10} {'Avg Time':<12}")
print("-" * 80)
for r in results_summary:
    print(f"{r['config']:<30} {r['accuracy']:.1%}        {r['ar_accuracy']:.1%}      {r['en_accuracy']:.1%}      {r['avg_time']*1000:.1f}ms")

# Performance improvements
baseline = results_summary[0]
best = results_summary[-1]

acc_improvement = (best['accuracy'] - baseline['accuracy']) * 100
time_reduction = ((baseline['avg_time'] - best['avg_time']) / baseline['avg_time']) * 100

print(f"\n{'='*80}")
print("IMPROVEMENTS")
print('='*80)
print(f"Accuracy Improvement: +{acc_improvement:.1f}% ({baseline['accuracy']:.1%} → {best['accuracy']:.1%})")
print(f"Time Reduction: {time_reduction:.1f}% ({baseline['avg_time']*1000:.1f}ms → {best['avg_time']*1000:.1f}ms)")

# Check if target met
print(f"\n{'='*80}")
print("TARGET ACHIEVEMENT")
print('='*80)
target_accuracy = 0.95
if best['accuracy'] >= target_accuracy:
    print(f"✅ TARGET MET: {best['accuracy']:.1%} >= {target_accuracy:.0%}")
else:
    print(f"❌ TARGET NOT MET: {best['accuracy']:.1%} < {target_accuracy:.0%}")
    print(f"   Gap: {(target_accuracy - best['accuracy'])*100:.1f}%")

# Save results
with open('index/test_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'summary': results_summary,
        'target_met': best['accuracy'] >= target_accuracy,
        'test_queries': len(test_queries)
    }, f, indent=2, ensure_ascii=False)

print(f"\n✅ Results saved to index/test_results.json")
print(f"\n{'='*80}")
print("TESTING COMPLETE")
print('='*80)
