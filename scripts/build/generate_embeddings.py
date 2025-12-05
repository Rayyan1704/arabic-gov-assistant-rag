"""Generate embeddings for all chunks"""
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 60)
print("🔢 Generating Embeddings for Corpus")
print("=" * 60)

# Load chunks
print("\n📥 Loading chunks...")
with open('index/corpus_chunks.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)

with open('index/corpus_meta.json', 'r', encoding='utf-8') as f:
    metadata = json.load(f)

print(f"✅ Loaded {len(chunks)} chunks")

# Load model
print("\n📥 Loading embedding model...")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
print("✅ Model loaded!")

# Generate embeddings (with progress bar)
print("\n🔢 Generating embeddings...")
embeddings = []

batch_size = 32
for i in tqdm(range(0, len(chunks), batch_size), desc="Processing batches"):
    batch = chunks[i:i+batch_size]
    batch_embeddings = model.encode(batch, show_progress_bar=False)
    embeddings.append(batch_embeddings)

embeddings = np.vstack(embeddings)

print(f"\n✅ Embeddings shape: {embeddings.shape}")
print(f"   Expected: ({len(chunks)}, 768)")

# Save
print("\n💾 Saving embeddings...")
np.save('index/embeddings.npy', embeddings)
print("✅ Saved to index/embeddings.npy")

# Quick test
print("\n" + "=" * 60)
print("🧪 Quick Test")
print("=" * 60)

test_query = "ما هي شروط الحصول على رخصة العمل؟"
query_embedding = model.encode([test_query])[0]

# Find most similar chunks
similarities = cosine_similarity([query_embedding], embeddings)[0]
top_5_idx = np.argsort(similarities)[-5:][::-1]

print(f"\nTest query: {test_query}")
print("\nTop 5 most similar chunks:")
for rank, idx in enumerate(top_5_idx, 1):
    print(f"\n[{rank}] Score: {similarities[idx]:.3f}")
    print(f"    Category: {metadata[idx]['category']}")
    print(f"    Text: {chunks[idx][:100]}...")

print("\n" + "=" * 60)
print("✅ Embeddings generation complete!")
print("=" * 60)
