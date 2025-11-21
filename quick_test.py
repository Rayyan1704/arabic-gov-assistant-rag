"""
Quick test of the RAG system (no API needed)
"""
import sys
sys.path.append('src')

from retrieval import RetrieverSystem
from sentence_transformers import SentenceTransformer

print("🚀 Loading Arabic Government Services RAG System...")
print("="*80)

# Load retriever
retriever = RetrieverSystem.load_index(
    'index/faiss.index',
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)

# Load embedding model
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
print("✅ System ready!\n")

def search(query, k=3):
    """Search for relevant documents"""
    query_emb = model.encode([query])[0]
    results = retriever.search(query_emb, k=k)
    return results

def display_results(query, results):
    """Display search results"""
    print(f"\n{'='*80}")
    print(f"السؤال: {query}")
    print('='*80)
    
    for r in results:
        print(f"\n[{r['rank']}] Score: {r['score']:.3f} | Category: {r['metadata']['category']}")
        print(f"File: {r['metadata']['source_file'].split('/')[-1]}")
        print(f"\n{r['chunk'][:300]}...")
        print("-" * 80)

# Test queries
test_queries = [
    "كيف أحصل على رخصة ليموزين؟",
    "ما هي خطوات تسجيل المقررات في جامعة قطر؟",
    "كيف أطلب استشارة طبية؟",
]

print("📝 Testing with sample queries...\n")

for query in test_queries:
    results = search(query)
    display_results(query, results)

print(f"\n{'='*80}")
print("✅ Test complete!")
print("="*80)
print("\nTo use interactively, run:")
print("  python -c \"from quick_test import search, display_results; display_results('your query', search('your query'))\"")
print("\nOr use the notebooks:")
print("  - notebooks/04_rag_with_gemini.ipynb (with API)")
print("  - notebooks/05_rag_no_api.ipynb (without API)")
