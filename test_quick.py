"""
Quick Comprehensive Test - Using existing models only
Tests 40 queries (20 Arabic + 20 English)
"""
import sys
sys.path.append('src')

import time
import numpy as np
from sentence_transformers import SentenceTransformer
from retrieval import RetrieverSystem
import json

print("="*80)
print("QUICK COMPREHENSIVE TEST")
print("40 Queries (20 Arabic + 20 English)")
print("="*80)

# Load models
print("\n[1/4] Loading models...")
start_time = time.time()
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
retriever = RetrieverSystem.load_index(
    'index/faiss.index',
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)
load_time = time.time() - start_time
print(f"✅ Models loaded in {load_time:.2f}s")

# Test queries - 40 total (20 Arabic + 20 English)
test_queries = [
    # Transportation - Arabic (5)
    {'query': 'كيف أحصل على رخصة ليموزين؟', 'expected': 'transportation', 'lang': 'ar'},
    {'query': 'ما هي خطوات تأجير السيارات؟', 'expected': 'transportation', 'lang': 'ar'},
    {'query': 'كيف أحصل على ترخيص نقل الأسماك؟', 'expected': 'transportation', 'lang': 'ar'},
    {'query': 'ما هي إجراءات الحصول على رخصة شحن جوي؟', 'expected': 'transportation', 'lang': 'ar'},
    {'query': 'كيف أطلب تعميم على مركبة؟', 'expected': 'transportation', 'lang': 'ar'},
    
    # Transportation - English (5)
    {'query': 'How do I get a limousine license in Qatar?', 'expected': 'transportation', 'lang': 'en'},
    {'query': 'What are the requirements for car rental?', 'expected': 'transportation', 'lang': 'en'},
    {'query': 'How to apply for air cargo license?', 'expected': 'transportation', 'lang': 'en'},
    {'query': 'Fish transport permit application', 'expected': 'transportation', 'lang': 'en'},
    {'query': 'Vehicle circulation request', 'expected': 'transportation', 'lang': 'en'},
    
    # Education - Arabic (5)
    {'query': 'كيف أسجل في مقررات جامعة قطر؟', 'expected': 'education', 'lang': 'ar'},
    {'query': 'ما هي خطوات طلب كشف الدرجات؟', 'expected': 'education', 'lang': 'ar'},
    {'query': 'كيف أتقدم للقبول في جامعة حمد بن خليفة؟', 'expected': 'education', 'lang': 'ar'},
    {'query': 'كيف أنسحب من جامعة قطر؟', 'expected': 'education', 'lang': 'ar'},
    {'query': 'أين أجد دليل المراكز البحثية؟', 'expected': 'education', 'lang': 'ar'},
    
    # Education - English (5)
    {'query': 'How to register for courses at Qatar University?', 'expected': 'education', 'lang': 'en'},
    {'query': 'Request transcript from QU', 'expected': 'education', 'lang': 'en'},
    {'query': 'HBKU admission application', 'expected': 'education', 'lang': 'en'},
    {'query': 'Withdraw from Qatar University', 'expected': 'education', 'lang': 'en'},
    {'query': 'Research centers guide Qatar', 'expected': 'education', 'lang': 'en'},
    
    # Health - Arabic (5)
    {'query': 'كيف أطلب استشارة طبية؟', 'expected': 'health', 'lang': 'ar'},
    {'query': 'كيف أحصل على تقرير طبي من حمد؟', 'expected': 'health', 'lang': 'ar'},
    {'query': 'كيف أتواصل مع مؤسسة حمد للاستشارات العاجلة؟', 'expected': 'health', 'lang': 'ar'},
    {'query': 'كيف أتقدم للتوظيف في مؤسسة حمد؟', 'expected': 'health', 'lang': 'ar'},
    {'query': 'كيف أحصل على ترخيص ممارس صحي؟', 'expected': 'health', 'lang': 'ar'},
    
    # Health - English (5)
    {'query': 'How to request medical consultation?', 'expected': 'health', 'lang': 'en'},
    {'query': 'Get medical report from Hamad', 'expected': 'health', 'lang': 'en'},
    {'query': 'Urgent medical consultation HMC', 'expected': 'health', 'lang': 'en'},
    {'query': 'Job application Hamad Medical', 'expected': 'health', 'lang': 'en'},
    {'query': 'Healthcare practitioner license', 'expected': 'health', 'lang': 'en'},
    
    # Business - Arabic (5)
    {'query': 'كيف أقدم عروض المناقصات؟', 'expected': 'business', 'lang': 'ar'},
    {'query': 'كيف أحصل على شهادة تأكيد استلام الطلب؟', 'expected': 'business', 'lang': 'ar'},
    {'query': 'كيف أسجل نفسي كمكلف في الضرائب؟', 'expected': 'business', 'lang': 'ar'},
    {'query': 'كيف أعيد تفعيل رخصة تجارية؟', 'expected': 'business', 'lang': 'ar'},
    {'query': 'كيف أحصل على تمويل من بنك قطر للتنمية؟', 'expected': 'business', 'lang': 'ar'},
    
    # Business - English (5)
    {'query': 'How to submit tenders in Qatar?', 'expected': 'business', 'lang': 'en'},
    {'query': 'CRA acknowledgement certificate', 'expected': 'business', 'lang': 'en'},
    {'query': 'Tax self-registration process', 'expected': 'business', 'lang': 'en'},
    {'query': 'Reactivate commercial license', 'expected': 'business', 'lang': 'en'},
    {'query': 'Company financing Qatar Development Bank', 'expected': 'business', 'lang': 'en'},
]

print(f"\n[2/4] Test set: {len(test_queries)} queries")
print(f"  Arabic: {sum(1 for q in test_queries if q['lang'] == 'ar')}")
print(f"  English: {sum(1 for q in test_queries if q['lang'] == 'en')}")

# Run tests
print(f"\n[3/4] Running tests...")
correct = 0
total_time = 0
results = []

for i, test in enumerate(test_queries, 1):
    start = time.time()
    
    # Get embedding and search
    query_emb = model.encode([test['query']])[0]
    search_results = retriever.search(query_emb, k=5)
    
    elapsed = time.time() - start
    total_time += elapsed
    
    # Check result
    top_category = search_results[0]['metadata']['category']
    is_correct = (top_category == test['expected'])
    if is_correct:
        correct += 1
    
    results.append({
        'query': test['query'],
        'lang': test['lang'],
        'expected': test['expected'],
        'got': top_category,
        'correct': is_correct,
        'time_ms': elapsed * 1000,
        'score': search_results[0]['score']
    })
    
    # Progress
    if i % 10 == 0:
        print(f"  Processed {i}/{len(test_queries)}...")

# Calculate metrics
print(f"\n[4/4] Calculating metrics...")

accuracy = correct / len(test_queries)
avg_time = total_time / len(test_queries)

# Language-specific
ar_results = [r for r in results if r['lang'] == 'ar']
en_results = [r for r in results if r['lang'] == 'en']

ar_correct = sum(1 for r in ar_results if r['correct'])
en_correct = sum(1 for r in en_results if r['correct'])

ar_accuracy = ar_correct / len(ar_results)
en_accuracy = en_correct / len(en_results)

# Category-specific
categories = set(r['expected'] for r in results)
cat_accuracy = {}
for cat in categories:
    cat_results = [r for r in results if r['expected'] == cat]
    cat_correct = sum(1 for r in cat_results if r['correct'])
    cat_accuracy[cat] = cat_correct / len(cat_results)

# Print results
print(f"\n{'='*80}")
print("RESULTS")
print('='*80)

print(f"\n📊 Overall Performance:")
print(f"  Accuracy: {accuracy:.1%} ({correct}/{len(test_queries)})")
print(f"  Avg Time: {avg_time*1000:.1f}ms")
print(f"  Total Time: {total_time:.2f}s")

print(f"\n🌍 Language Performance:")
print(f"  Arabic:  {ar_accuracy:.1%} ({ar_correct}/{len(ar_results)})")
print(f"  English: {en_accuracy:.1%} ({en_correct}/{len(en_results)})")

print(f"\n📁 Category Performance:")
for cat in sorted(categories):
    print(f"  {cat:15s}: {cat_accuracy[cat]:.1%}")

# Failed queries
failed = [r for r in results if not r['correct']]
if failed:
    print(f"\n❌ Failed Queries ({len(failed)}):")
    for f in failed:
        print(f"  {f['lang'].upper()}: {f['query'][:50]}...")
        print(f"      Expected: {f['expected']} | Got: {f['got']} | Score: {f['score']:.3f}")

# Performance stats
print(f"\n⚡ Performance Stats:")
print(f"  Min Time: {min(r['time_ms'] for r in results):.1f}ms")
print(f"  Max Time: {max(r['time_ms'] for r in results):.1f}ms")
print(f"  Avg Time: {avg_time*1000:.1f}ms")
print(f"  Median Time: {np.median([r['time_ms'] for r in results]):.1f}ms")

# Target check
print(f"\n{'='*80}")
print("TARGET ACHIEVEMENT")
print('='*80)
target = 0.95
if accuracy >= target:
    print(f"✅ TARGET MET: {accuracy:.1%} >= {target:.0%}")
else:
    gap = (target - accuracy) * 100
    print(f"⚠️  TARGET: {accuracy:.1%} (Gap: {gap:.1f}%)")
    print(f"   Need {int(gap * len(test_queries) / 100)} more correct answers")

# Save results
output = {
    'overall_accuracy': accuracy,
    'arabic_accuracy': ar_accuracy,
    'english_accuracy': en_accuracy,
    'category_accuracy': cat_accuracy,
    'avg_time_ms': avg_time * 1000,
    'total_queries': len(test_queries),
    'correct': correct,
    'target_met': accuracy >= target,
    'details': results
}

with open('index/quick_test_results.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Results saved to index/quick_test_results.json")
print(f"\n{'='*80}")
print("TEST COMPLETE")
print('='*80)
