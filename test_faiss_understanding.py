"""Test understanding of FAISS"""
import faiss
import numpy as np

print("=" * 60)
print("🧪 Testing FAISS Understanding")
print("=" * 60)

# Create sample data
d = 768  # dimension
n = 1000  # number of vectors
vectors = np.random.random((n, d)).astype('float32')

print(f"\n📊 Created {n} random vectors of dimension {d}")

# Normalize (for cosine similarity)
faiss.normalize_L2(vectors)
print("✅ Normalized vectors for cosine similarity")

# Create index
index = faiss.IndexFlatIP(d)  # IP = Inner Product (cosine for normalized vectors)
index.add(vectors)

print(f"✅ Index created and populated")
print(f"   Index contains {index.ntotal} vectors")

# Search
query = np.random.random((1, d)).astype('float32')
faiss.normalize_L2(query)

k = 5
distances, indices = index.search(query, k)

print(f"\n🔍 Searching for top {k} neighbors...")
print(f"\nTop {k} neighbors:")
print(f"Indices: {indices[0]}")
print(f"Scores: {distances[0]}")

print("\n" + "=" * 60)
print("📈 Key Concepts:")
print("=" * 60)
print("✅ IndexFlatIP: Inner Product index (exact search)")
print("✅ normalize_L2: Normalize vectors for cosine similarity")
print("✅ k: Number of neighbors to return")
print("✅ Scores: Higher = more similar (for Inner Product)")

print("\n" + "=" * 60)
print("✅ FAISS understanding test complete!")
print("=" * 60)
