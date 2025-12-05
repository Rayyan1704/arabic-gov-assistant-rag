"""Process all documents into chunks"""
import sys
from pathlib import Path
sys.path.append('src')

from src.chunking import chunk_document
import glob
import json

# Create index directory
Path('index').mkdir(exist_ok=True)

# Process all documents
all_chunks = []
metadata = []

categories = ['health', 'education', 'business', 'transportation', 'justice', 'housing', 'culture', 'info']

print("Processing documents...")
print("=" * 60)

for cat in categories:
    files = glob.glob(f'data/{cat}/*.txt')
    print(f"\n📁 {cat}: {len(files)} files")
    
    for filepath in files:
        try:
            chunks = chunk_document(filepath, chunk_size=512, overlap=128)
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                metadata.append({
                    'source_file': filepath,
                    'category': cat,
                    'chunk_id': i,
                    'chunk_length': len(chunk)
                })
            
            print(f"  ✅ {Path(filepath).name}: {len(chunks)} chunks")
        except Exception as e:
            print(f"  ❌ {Path(filepath).name}: {e}")

print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print(f"Total documents: {len(set(m['source_file'] for m in metadata))}")
print(f"Total chunks: {len(all_chunks)}")
print(f"\nChunks per category:")
for cat in categories:
    count = len([m for m in metadata if m['category'] == cat])
    print(f"  {cat}: {count}")

# Save
print("\n💾 Saving to index/ directory...")
with open('index/corpus_chunks.json', 'w', encoding='utf-8') as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

with open('index/corpus_meta.json', 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("✅ Saved:")
print("  - index/corpus_chunks.json")
print("  - index/corpus_meta.json")
print("\n" + "=" * 60)
print("✅ ALL DOCUMENTS PROCESSED!")
print("=" * 60)
