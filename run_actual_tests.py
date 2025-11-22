"""
ACTUAL TEST EXECUTION - Run real tests with existing models
"""
import sys
sys.path.append('src')

import time
import numpy as np
import json
from retrieval import RetrieverSystem

print("="*80)
print("RUNNING ACTUAL TESTS")
print("="*80)

# Check if models exist
import os
if not os.path.exists('index/embeddings.npy'):
    print("❌ embeddings.npy not found. Run notebooks 01-02 first.")
    exit(1)

if not os.path.exists('index/faiss.index'):
    print("❌ faiss.index not found. Run notebook 03 first.")
    exit(1)

print("\n✅ Found existing models")

# Load retriever
print("\n[1/3] Loading retriever...")
retriever = RetrieverSystem.load_index(
    'index/faiss.index',
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)

# Load embedding model
print("[2/3] Loading embedding model...")
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
print("✅ Models loaded")

# Test queries - 20 total (10 Arabic + 10 English)
test_queries = [
    # Transportation
    {'query': 'كيف أحصل على رخصة ليموزين؟', 'expected': 'transportation', 'lang': 'ar'},
    {'query': 'How do I get a limousine license?', 'expected': 'transportation', 'lang': 'en'},
    
    # Education
    {'query': 'كيف أسجل في مقررات جامعة قطر؟', 'expected': 'education', 'lang': 'ar'},
    {'query': 'How to register for courses at Qatar University?', 'expected': 'education', 'lang': 'en'},
    {'query': 'ما هي خطوات طلب كشف الدرجات؟', 'expected': 'education', 'lang': 'ar'},
    {'query': 'Request transcript from QU', 'expected': 'education', 'lang': 'en'},
    
    # Health
    {'query': 'كيف أطلب استشارة طبية؟', 'expected': 'health', 'lang': 'ar'},
    {'query': 'How to request medical consultation?', 'expected': 'health', 'lang': 'en'},
    {'query': 'كيف أحصل على تقرير طبي من حمد؟', 'expected': 'health', 'lang': 'ar'},
    {'query': 'Get medical report from Hamad', 'expected': 'health', 'lang': 'en'},
    
    # Business
    {'query': 'كيف أقدم عروض المناقصات؟', 'expected': 'business', 'lang': 'ar'},
    {'query': 'How to submit tenders?', 'expected': 'business', 'lang': 'en'},
    {'query': 'كيف أحصل على شهادة CRA؟', 'expected': 'business', 'lang': 'ar'},
    {'query': 'CRA certificate request', 'expected': 'business', 'lang': 'en'},
    
    # Transportation
    {'query': 'ما هي إجراءات الحصول على رخصة شحن جوي؟', 'expected': 'transportation', 'lang': 'ar'},
    {'query': 'Air cargo license application', 'expected': 'transportation', 'lang': 'en'},
    
    # Education
    {'query': 'كيف أنسحب من جامعة قطر؟', 'expected': 'education', 'lang': 'ar'},
    {'query': 'Withdraw from Qatar University', 'expected': 'education', 'lang': 'en'},
    
    # Health
    {'query': 'كيف أتقدم للتوظيف في مؤسسة حمد؟', 'expected': 'health', 'lang': 'ar'},
    {'query': 'Job application Hamad Medical', 'expected': 'health', 'lang': 'en'},
]

print(f"\n[3/3] Running tests on {len(test_queries)} queries...")

# Run tests
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
        'score': search_results[0]['score'],
        'top_3_categories': [r['metadata']['category'] for r in search_results[:3]]
    })
    
    status = "✅" if is_correct else "❌"
    print(f"  {status} [{i}/{len(test_queries)}] {test['lang'].upper()}: {test['query'][:40]}...")

# Calculate metrics
accuracy = correct / len(test_queries)
avg_time = total_time / len(test_queries)

ar_results = [r for r in results if r['lang'] == 'ar']
en_results = [r for r in results if r['lang'] == 'en']
ar_correct = sum(1 for r in ar_results if r['correct'])
en_correct = sum(1 for r in en_results if r['correct'])
ar_accuracy = ar_correct / len(ar_results) if ar_results else 0
en_accuracy = en_correct / len(en_results) if en_results else 0

# Calculate P@3
p_at_3_scores = []
for r in results:
    relevant_in_top_3 = sum(1 for cat in r['top_3_categories'] if cat == r['expected'])
    p_at_3_scores.append(relevant_in_top_3 / 3)
p_at_3 = np.mean(p_at_3_scores)

# Calculate MRR
mrr_scores = []
for r in results:
    try:
        rank = r['top_3_categories'].index(r['expected']) + 1
        mrr_scores.append(1.0 / rank)
    except ValueError:
        mrr_scores.append(0)
mrr = np.mean(mrr_scores)

# Print results
print(f"\n{'='*80}")
print("ACTUAL TEST RESULTS")
print('='*80)

print(f"\n📊 Overall Performance:")
print(f"  Accuracy (P@1): {accuracy:.1%} ({correct}/{len(test_queries)})")
print(f"  Precision@3:    {p_at_3:.1%}")
print(f"  MRR:            {mrr:.3f}")
print(f"  Avg Time:       {avg_time*1000:.1f}ms")

print(f"\n🌍 Language Performance:")
print(f"  Arabic:  {ar_accuracy:.1%} ({ar_correct}/{len(ar_results)})")
print(f"  English: {en_accuracy:.1%} ({en_correct}/{len(en_results)})")

# Failed queries
failed = [r for r in results if not r['correct']]
if failed:
    print(f"\n❌ Failed Queries ({len(failed)}):")
    for f in failed:
        print(f"  {f['lang'].upper()}: {f['query']}")
        print(f"      Expected: {f['expected']} | Got: {f['got']} | Score: {f['score']:.3f}")

# Save results
output = {
    'test_date': time.strftime('%Y-%m-%d %H:%M:%S'),
    'total_queries': len(test_queries),
    'correct': correct,
    'accuracy': accuracy,
    'precision_at_3': p_at_3,
    'mrr': mrr,
    'avg_time_ms': avg_time * 1000,
    'arabic_accuracy': ar_accuracy,
    'english_accuracy': en_accuracy,
    'details': results
}

with open('index/actual_test_results.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Results saved to index/actual_test_results.json")

# Target check
print(f"\n{'='*80}")
print("TARGET CHECK")
print('='*80)
target = 0.95
if accuracy >= target:
    print(f"✅ TARGET MET: {accuracy:.1%} >= {target:.0%}")
else:
    gap = (target - accuracy) * 100
    print(f"⚠️  CURRENT: {accuracy:.1%} (Gap: {gap:.1f}%)")
    print(f"   Need {int(np.ceil(gap * len(test_queries) / 100))} more correct")

print(f"\n{'='*80}")
print("TEST COMPLETE")
print('='*80)
