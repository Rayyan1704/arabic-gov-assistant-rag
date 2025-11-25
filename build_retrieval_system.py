"""Build and test retrieval system"""
from src.retrieval import RetrieverSystem
from sentence_transformers import SentenceTransformer

print("=" * 60)
print("🔧 Building Retrieval System")
print("=" * 60)

# Build retriever
print("\n📥 Loading data and building index...")
retriever = RetrieverSystem(
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)

# Save index
print("\n💾 Saving FAISS index...")
retriever.save_index('index/faiss.index')

# Show stats
print("\n📊 System Statistics:")
stats = retriever.get_stats()
print(f"  Total chunks: {stats['total_chunks']}")
print(f"  Total documents: {stats['total_documents']}")
print(f"  Embedding dimension: {stats['embedding_dim']}")
print(f"\n  Chunks per category:")
for cat, count in sorted(stats['categories'].items()):
    print(f"    {cat}: {count}")

# Load model for queries
print("\n📥 Loading query model...")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Test queries
test_queries = [
    "كيف أحصل على رخصة قيادة في قطر؟",
    "ما هي إجراءات فتح شركة جديدة؟",
    "كيف أسجل أطفالي في المدرسة؟",
]

print("\n" + "=" * 60)
print("🧪 Testing Retrieval")
print("=" * 60)

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print('='*60)
    
    # Get query embedding
    query_emb = model.encode([query])[0]
    
    # Search
    results = retriever.search(query_emb, k=5)
    
    # Display
    for r in results:
        print(f"\n[Rank {r['rank']}] Score: {r['score']:.3f}")
        print(f"Category: {r['metadata']['category']}")
        print(f"Source: {r['metadata']['source_file']}")
        print(f"Text: {r['chunk'][:150]}...")

print("\n" + "=" * 60)
print("✅ Retrieval system built and tested!")
print("=" * 60)
