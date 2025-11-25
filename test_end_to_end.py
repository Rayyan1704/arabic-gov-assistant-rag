"""Test complete RAG pipeline end-to-end"""
from src.llm_generator import AnswerGenerator
from src.retrieval import RetrieverSystem
from sentence_transformers import SentenceTransformer

print("=" * 60)
print("🚀 Testing Complete RAG Pipeline")
print("=" * 60)

# Load everything
print("\n📥 Loading components...")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
print("✅ Embedding model loaded")

retriever = RetrieverSystem.load_index(
    'index/faiss.index',
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)

generator = AnswerGenerator()

# Test queries
test_queries = [
    "كيف أحصل على رخصة قيادة في قطر؟",
    "ما هي إجراءات فتح شركة جديدة؟",
    "كيف أسجل أطفالي في المدرسة؟"
]

print("\n" + "=" * 60)
print("🧪 Testing End-to-End RAG")
print("=" * 60)

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"📝 Query: {query}")
    print('='*60)
    
    # Step 1: Retrieve
    print("\n🔍 Step 1: Retrieving relevant documents...")
    query_emb = model.encode([query])[0]
    contexts = retriever.search(query_emb, k=10)
    print(f"✅ Retrieved {len(contexts)} documents")
    
    # Show top 3
    print("\nTop 3 results:")
    for i, ctx in enumerate(contexts[:3], 1):
        print(f"  {i}. {ctx['metadata']['category']} (score: {ctx['score']:.3f})")
    
    # Step 2: Generate answer
    print("\n🤖 Step 2: Generating answer with Gemini...")
    result = generator.generate_answer(query, contexts)
    
    # Display
    print("\n📄 Answer:")
    print("-" * 60)
    print(result['answer'])
    print("-" * 60)
    
    print("\n📚 Sources:")
    for i, src in enumerate(result['sources'], 1):
        print(f"  {i}. {src['category']} - {src['file']} (score: {src['score']:.3f})")
    
    print("\n" + "=" * 60)

print("\n✅ End-to-end RAG pipeline test complete!")
print("=" * 60)
