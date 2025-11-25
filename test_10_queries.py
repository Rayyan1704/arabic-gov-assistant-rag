"""Test system with 10 diverse queries"""
from src.llm_generator import AnswerGenerator
from src.retrieval import RetrieverSystem
from sentence_transformers import SentenceTransformer
import json

print("=" * 80)
print("🧪 Testing with 10 Diverse Queries")
print("=" * 80)

# Load components
print("\n📥 Loading components...")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
retriever = RetrieverSystem.load_index(
    'index/faiss.index',
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)
generator = AnswerGenerator()

# 10 diverse test queries covering all categories
test_queries = [
    {
        'id': 1,
        'query': 'كيف أحصل على رخصة قيادة في قطر؟',
        'expected_category': 'transportation',
        'description': 'Driving license'
    },
    {
        'id': 2,
        'query': 'ما هي إجراءات فتح سجل تجاري؟',
        'expected_category': 'business',
        'description': 'Commercial registration'
    },
    {
        'id': 3,
        'query': 'كيف أسجل أطفالي في المدرسة؟',
        'expected_category': 'education',
        'description': 'School registration'
    },
    {
        'id': 4,
        'query': 'كيف أحصل على استشارة طبية؟',
        'expected_category': 'health',
        'description': 'Medical consultation'
    },
    {
        'id': 5,
        'query': 'ما هي خطوات الحصول على ترخيص بناء؟',
        'expected_category': 'housing',
        'description': 'Building permit'
    },
    {
        'id': 6,
        'query': 'كيف أبحث عن قضية في المحكمة؟',
        'expected_category': 'justice',
        'description': 'Court case search'
    },
    {
        'id': 7,
        'query': 'كيف أحصل على تصريح تصوير فيلم؟',
        'expected_category': 'culture',
        'description': 'Film shooting permit'
    },
    {
        'id': 8,
        'query': 'ما هي معلومات الاتصال بالحكومة؟',
        'expected_category': 'info',
        'description': 'Government contact info'
    },
    {
        'id': 9,
        'query': 'كيف أطلب كشف درجات من الجامعة؟',
        'expected_category': 'education',
        'description': 'University transcript'
    },
    {
        'id': 10,
        'query': 'ما هي شروط الحصول على تمويل للشركات؟',
        'expected_category': 'business',
        'description': 'Business financing'
    }
]

results = []

for test in test_queries:
    print(f"\n{'='*80}")
    print(f"Query {test['id']}: {test['query']}")
    print(f"Expected: {test['expected_category']} ({test['description']})")
    print('='*80)
    
    # Retrieve
    query_emb = model.encode([test['query']])[0]
    contexts = retriever.search(query_emb, k=10)
    
    # Check top results
    top_3_categories = [ctx['metadata']['category'] for ctx in contexts[:3]]
    top_1_category = top_3_categories[0]
    
    # Calculate metrics
    correct_at_1 = top_1_category == test['expected_category']
    correct_in_3 = test['expected_category'] in top_3_categories
    
    print(f"\n🔍 Retrieval:")
    print(f"  Top-1: {top_1_category} (score: {contexts[0]['score']:.3f}) {'✅' if correct_at_1 else '❌'}")
    print(f"  Top-3: {top_3_categories} {'✅' if correct_in_3 else '❌'}")
    
    # Generate answer
    result = generator.generate_answer(test['query'], contexts)
    
    print(f"\n📄 Answer (first 200 chars):")
    print(f"  {result['answer'][:200]}...")
    
    # Store results
    results.append({
        'query_id': test['id'],
        'query': test['query'],
        'expected_category': test['expected_category'],
        'top_1_category': top_1_category,
        'top_3_categories': top_3_categories,
        'correct_at_1': correct_at_1,
        'correct_in_3': correct_in_3,
        'top_1_score': float(contexts[0]['score']),
        'answer_length': len(result['answer'])
    })

# Calculate overall metrics
print("\n" + "=" * 80)
print("📊 OVERALL METRICS")
print("=" * 80)

precision_at_1 = sum(r['correct_at_1'] for r in results) / len(results)
precision_at_3 = sum(r['correct_in_3'] for r in results) / len(results)
avg_score = sum(r['top_1_score'] for r in results) / len(results)
avg_answer_length = sum(r['answer_length'] for r in results) / len(results)

print(f"\nPrecision@1: {precision_at_1:.2%} ({sum(r['correct_at_1'] for r in results)}/{len(results)})")
print(f"Precision@3: {precision_at_3:.2%} ({sum(r['correct_in_3'] for r in results)}/{len(results)})")
print(f"Average Top-1 Score: {avg_score:.3f}")
print(f"Average Answer Length: {avg_answer_length:.0f} characters")

# Category breakdown
print(f"\n📁 Category Breakdown:")
from collections import Counter
expected_cats = Counter(r['expected_category'] for r in results)
for cat, count in sorted(expected_cats.items()):
    correct = sum(1 for r in results if r['expected_category'] == cat and r['correct_at_1'])
    print(f"  {cat}: {correct}/{count} correct")

# Save results
with open('index/test_10_queries_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'queries': results,
        'metrics': {
            'precision_at_1': precision_at_1,
            'precision_at_3': precision_at_3,
            'avg_score': avg_score,
            'avg_answer_length': avg_answer_length
        }
    }, f, ensure_ascii=False, indent=2)

print(f"\n✅ Results saved to index/test_10_queries_results.json")
print("=" * 80)
