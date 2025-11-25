"""
Rebuild the entire system with optimizations
This will create a new, better index
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path
import re
from tqdm import tqdm


class OptimizedPreprocessor:
    """Improved preprocessing"""
    
    @staticmethod
    def normalize_arabic_light(text: str) -> str:
        """Light normalization"""
        if not text:
            return ""
        
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)  # Remove diacritics
        text = re.sub(r'[إأآ]', 'ا', text)  # Normalize alef only
        text = re.sub(r'\s+', ' ', text)  # Clean spaces
        
        return text.strip()
    
    @staticmethod
    def remove_boilerplate(text: str) -> str:
        """Remove generic boilerplate"""
        patterns = [
            r'تقدم .+ خدمه .+ بهدف تسهيل حصول المستفيدين علي الاجراءات المطلوبه بطريقه سريعه وموثوقه\.',
            r'تمكن هذه الخدمه المستفيدين من اكمال المعاملات ذات العلاقه عبر قنوات مخصصه.+?الخدمه\.',
            r'تراعي في تقديم الخدمه دقه البيانات واحترام سريه المعلومات الشخصيه للمستفيدين\.',
            r'تشمل خطوات الاستفاده من الخدمه جمع المستندات المطلوبه.+?الخدمه\.',
            r'تعمل الجهه المختصه علي مراجعه الطلبات خلال المدد الزمنيه المعلنه.+?الرسميه\.',
            r'ينبغي علي المتقدم الالتزام بالشروط والتعليمات الوارده في صفحه الخدمه.+?الخدمه\.',
            r'كما ينصح بالاحتفاظ بنسخ من المستندات المقدمه.+?الخدمه\.',
            r'التحقق من استيفاء الشروط والمستندات المطلوبه\.',
            r'تجهيز المستندات بصيغتها الاصليه او المصوره حسب المطلوب\.',
            r'تعبئه النموذج الالكتروني بدقه وارفاق المستندات المطلوبه\.',
            r'مراجعه البيانات قبل الارسال والتاكد من صحه الوسيله للتواصل\.',
            r'متابعه حاله الطلب والرد علي اي طلب توضيحي من الجهه المقدمه\.',
            r'تختلف الرسوم بحسب نوع المعامله وحاله المتقدم.+?التقديم\.',
            r'صوره من البطاقه الشخصيه او جواز السفر\.',
            r'المستندات الداعمه الخاصه بطبيعه الطلب مثل السجل التجاري او مستند اثبات العلاقه\.',
            r'نماذج او استمارات تعبئه حسب مواصفات الخدمه\.',
            r'لمزيد من المعلومات يرجي مراجعه الجهه المختصه او دليل الخدمه الرسمي\.',
            r'قد تطبق شروط اضافيه او استثناءات وفقا لطبيعه الطلب واعتبارات الجهه المقدمه\.'
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL)
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n', text)
        
        return text.strip()
    
    @staticmethod
    def boost_title(text: str) -> str:
        """Boost title by repeating it"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if not lines:
            return text
        
        title = lines[0]
        # Repeat title 2x for emphasis
        boosted = f"{title}\n{title}\n" + '\n'.join(lines)
        
        return boosted


def chunk_optimized(text: str, chunk_size=400, overlap=80) -> list:
    """Optimized chunking - smaller, more specific"""
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 30]
    
    chunks = []
    current = ""
    
    for para in paragraphs:
        if len(current) + len(para) < chunk_size:
            current += "\n\n" + para if current else para
        else:
            if len(current) >= chunk_size - 100:
                chunks.append(current.strip())
            
            if overlap > 0 and current:
                overlap_text = current[-overlap:]
                current = overlap_text + "\n\n" + para
            else:
                current = para
    
    if len(current) >= chunk_size - 100:
        chunks.append(current.strip())
    
    return chunks


def rebuild_system():
    """Rebuild entire system with optimizations"""
    
    print("="*80)
    print("REBUILDING OPTIMIZED SYSTEM")
    print("="*80)
    
    preprocessor = OptimizedPreprocessor()
    
    # Load documents
    print("\n1. Loading documents...")
    data_dir = Path('data')
    documents = []
    
    for category_dir in sorted(data_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name == 'archive_backup':
            continue
        
        category = category_dir.name
        
        for filepath in category_dir.glob("*.txt"):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if text:
                documents.append({
                    'text': text,
                    'category': category,
                    'filename': filepath.name
                })
    
    print(f"   Loaded {len(documents)} documents")
    
    # Process and chunk
    print("\n2. Processing with optimizations...")
    all_chunks = []
    all_metadata = []
    
    for doc in tqdm(documents, desc="Processing"):
        # Apply optimizations
        text = preprocessor.normalize_arabic_light(doc['text'])
        text = preprocessor.remove_boilerplate(text)
        text = preprocessor.boost_title(text)
        
        # Chunk with smaller size
        chunks = chunk_optimized(text, chunk_size=400, overlap=80)
        
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadata.append({
                'category': doc['category'],
                'source_file': doc['filename']
            })
    
    print(f"   Created {len(all_chunks)} optimized chunks")
    
    # Generate embeddings
    print("\n3. Generating embeddings...")
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    embeddings = []
    batch_size = 32
    
    for i in tqdm(range(0, len(all_chunks), batch_size), desc="Embedding"):
        batch = all_chunks[i:i+batch_size]
        batch_emb = model.encode(batch, show_progress_bar=False)
        embeddings.append(batch_emb)
    
    embeddings = np.vstack(embeddings).astype('float32')
    
    # Normalize
    faiss.normalize_L2(embeddings)
    
    # Save
    print("\n4. Saving optimized index...")
    np.save('index/embeddings_optimized.npy', embeddings)
    
    with open('index/corpus_chunks_optimized.json', 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    
    with open('index/corpus_meta_optimized.json', 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, ensure_ascii=False, indent=2)
    
    # Build FAISS index
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)
    faiss.write_index(index, 'index/faiss_optimized.index')
    
    print(f"\n[OK] Optimized system built!")
    print(f"   Chunks: {len(all_chunks)}")
    print(f"   Embeddings: {embeddings.shape}")
    print(f"   Files saved with '_optimized' suffix")
    
    return {
        'chunks': len(all_chunks),
        'documents': len(documents)
    }


if __name__ == "__main__":
    results = rebuild_system()
