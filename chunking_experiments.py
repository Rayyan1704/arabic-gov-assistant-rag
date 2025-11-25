"""Chunking experiments - test different chunk sizes"""
import sys
sys.path.append('src')

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
from tqdm import tqdm
import glob
from pathlib import Path

print("=" * 80)
print("🔬 CHUNKING EXPERIMENTS")
print("=" * 80)

# Load model
print("\n📥 Loading embedding model...")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Test queries with expected categories
test_queries = [
    {'query': 'كيف أحصل على رخصة قيادة؟', 'expected_category': 'transportation'},
    {'query': 'ما هي إجراءات فتح سجل تجاري؟', 'expected_category': 'business'},
    {'query': 'كيف أسجل أطفالي في المدرسة؟', 'expected_category': 'education'},
    {'query': 'كيف أحصل على استشارة طبية؟', 'expected_category': 'health'},
    {'query': 'ما هي خطوات الحصول على ترخيص بناء؟', 'expected_category': 'housing'},
    {'query': 'كيف أبحث عن قضية في المحكمة؟', 'expected_category': 'justice'},
    {'query': 'كيف أحصل على تصريح تصوير فيلم؟', 'expected_category': 'culture'},
    {'query': 'ما هي معلومات الاتصال بالحكومة؟', 'expected_category': 'info'},
    {'query': 'كيف أطلب كشف درجات من الجامعة؟', 'expected_category': 'education'},
    {'query': 'ما هي شروط الحصول على تمويل للشركات؟', 'expected_category': 'business'},
]

def chunk_document_custom(filepath, chunk_size=512, overlap=128):
    """Chunk document with custom parameters"""
    import re
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Clean
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = text.split('\n')
    lines = [l for l in lines if len(l.strip()) > 10]
    text = '\n'.join(lines)
    
    # Normalize Arabic
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u0600-\u06FF\s\d\.\،\؛\؟]', '', text)
    text = text.strip()
    
    # Chunk by paragraphs
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    chunks = []
    current_chunk = ""
    min_chunk_size = chunk_size - 100
    max_chunk_size = chunk_size + 100
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < max_chunk_size:
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            if len(current_chunk) >= min_chunk_size:
                chunks.append(current_chunk.strip())
                
            if overlap > 0 and current_chunk:
                overlap_text = current_chunk[-overlap:]
                current_chunk = overlap_text + "\n\n" + para
            else:
                current_chunk = para
    
    if len(current_chunk) >= min_chunk_size:
        chunks.append(current_chunk.strip())
    
    return chunks

def evaluate_retrieval(chunks, embeddings, metadata, test_queries, k=5):
    """Evaluate retrieval quality"""
    results = {
        'precision_at_1': [],
        'precision_at_3': [],
        'precision_at_5': [],
        'mrr': []
    }
    
    for test in test_queries:
        query = test['query']
        expected_cat = test['expected_category']
        
        # Get query embedding
        query_emb = model.encode([query])
        
        # Calculate similarities
        sims = cosine_similarity(query_emb, embeddings)[0]
        top_k_idx = np.argsort(sims)[-k:][::-1]
        
        # Check if expected category appears in top results
        retrieved_cats = [metadata[idx]['category'] for idx in top_k_idx]
        
        # Precision@1
        p_at_1 = 1 if retrieved_cats[0] == expected_cat else 0
        results['precision_at_1'].append(p_at_1)
        
        # Precision@3
        p_at_3 = sum(1 for c in retrieved_cats[:3] if c == expected_cat) / 3
        results['precision_at_3'].append(p_at_3)
        
        # Precision@5
        p_at_5 = sum(1 for c in retrieved_cats[:5] if c == expected_cat) / 5
        results['precision_at_5'].append(p_at_5)
        
        # MRR
        try:
            first_relevant = retrieved_cats.index(expected_cat) + 1
            mrr = 1.0 / first_relevant
        except ValueError:
            mrr = 0
        results['mrr'].append(mrr)
    
    # Calculate averages
    return {
        'P@1': np.mean(results['precision_at_1']),
        'P@3': np.mean(results['precision_at_3']),
        'P@5': np.mean(results['precision_at_5']),
        'MRR': np.mean(results['mrr'])
    }

# Experiment with different chunk sizes
chunk_configs = [
    {'size': 256, 'overlap': 64},
    {'size': 512, 'overlap': 128},
    {'size': 768, 'overlap': 192},
    {'size': 1024, 'overlap': 256},
]

experiment_results = []
categories = ['health', 'education', 'business', 'transportation', 'justice', 'housing', 'culture', 'info']

for config in chunk_configs:
    print(f"\n{'='*80}")
    print(f"🔬 Testing: chunk_size={config['size']}, overlap={config['overlap']}")
    print('='*80)
    
    # Re-chunk all documents with this config
    all_chunks = []
    metadata = []
    
    for cat in categories:
        files = glob.glob(f'data/{cat}/*.txt')
        for filepath in files:
            chunks = chunk_document_custom(filepath,
                                          chunk_size=config['size'],
                                          overlap=config['overlap'])
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                metadata.append({
                    'source_file': filepath,
                    'category': cat,
                    'chunk_id': i
                })
    
    print(f"  📊 Generated {len(all_chunks)} chunks")
    
    # Generate embeddings
    print(f"  🔢 Generating embeddings...")
    embeddings = model.encode(all_chunks, show_progress_bar=True, batch_size=32)
    
    # Evaluate
    print("  📈 Evaluating...")
    metrics = evaluate_retrieval(all_chunks, embeddings, metadata, test_queries)
    
    result = {
        'config': config,
        'num_chunks': len(all_chunks),
        'metrics': metrics
    }
    experiment_results.append(result)
    
    print(f"\n  ✅ Results:")
    print(f"     P@1: {metrics['P@1']:.3f}")
    print(f"     P@3: {metrics['P@3']:.3f}")
    print(f"     P@5: {metrics['P@5']:.3f}")
    print(f"     MRR: {metrics['MRR']:.3f}")

# Display results table
print("\n" + "=" * 80)
print("📊 CHUNKING EXPERIMENTS RESULTS")
print("=" * 80)

print(f"\n{'Chunk Size':<12} {'Overlap':<10} {'Chunks':<10} {'P@1':<8} {'P@3':<8} {'P@5':<8} {'MRR':<8}")
print("-" * 80)
for r in experiment_results:
    print(f"{r['config']['size']:<12} {r['config']['overlap']:<10} {r['num_chunks']:<10} "
          f"{r['metrics']['P@1']:<8.3f} {r['metrics']['P@3']:<8.3f} "
          f"{r['metrics']['P@5']:<8.3f} {r['metrics']['MRR']:<8.3f}")

# Find best configuration
best_config = max(experiment_results, key=lambda x: x['metrics']['MRR'])
print(f"\n🏆 Best Configuration:")
print(f"   Chunk Size: {best_config['config']['size']}")
print(f"   Overlap: {best_config['config']['overlap']}")
print(f"   MRR: {best_config['metrics']['MRR']:.3f}")

# Save results
with open('index/experiment_results.json', 'w', encoding='utf-8') as f:
    json.dump(experiment_results, f, ensure_ascii=False, indent=2)

print(f"\n✅ Results saved to index/experiment_results.json")
print("=" * 80)
