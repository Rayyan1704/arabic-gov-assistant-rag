"""Test understanding of embeddings"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 60)
print("🧪 Testing Embeddings Understanding")
print("=" * 60)

# Load model
print("\n📥 Loading model...")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
print("✅ Model loaded!")

# Test texts
texts = [
    "كيف أحصل على رخصة قيادة؟",  # How do I get a driver's license?
    "ما هي متطلبات رخصة السياقة؟",  # What are driving license requirements?
    "أريد تجديد جواز السفر"  # I want to renew passport (different topic)
]

print("\n📝 Test texts:")
for i, text in enumerate(texts, 1):
    print(f"  {i}. {text}")

# Generate embeddings
print("\n🔢 Generating embeddings...")
embeddings = model.encode(texts)
print(f"✅ Shape: {embeddings.shape}")  # Should be (3, 768)

# Calculate cosine similarity
print("\n📊 Calculating similarity matrix...")
sim_matrix = cosine_similarity(embeddings)

print("\nSimilarity Matrix:")
print("=" * 60)
for i in range(len(texts)):
    for j in range(len(texts)):
        print(f"Text {i+1} vs Text {j+1}: {sim_matrix[i][j]:.4f}")

print("\n" + "=" * 60)
print("📈 Analysis:")
print("=" * 60)
print(f"Similarity between texts 1 & 2 (both about driving): {sim_matrix[0][1]:.4f}")
print(f"Similarity between texts 1 & 3 (different topics): {sim_matrix[0][2]:.4f}")
print(f"Similarity between texts 2 & 3 (different topics): {sim_matrix[1][2]:.4f}")

if sim_matrix[0][1] > sim_matrix[0][2]:
    print("\n✅ CORRECT: Texts about same topic are more similar!")
else:
    print("\n❌ UNEXPECTED: Check the model or texts")

print("\n" + "=" * 60)
print("✅ Embeddings understanding test complete!")
print("=" * 60)
