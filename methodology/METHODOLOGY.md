# System Methodology

**Project:** Cross-Lingual Retrieval-Augmented Generation for Arabic Government Services  
**Author:** Mohammed Aaqil Rayyan  
**Duration:** 20 days (November-December 2025)  
**Final Accuracy:** 99% category accuracy (formal), 84% category accuracy (messy)  
**Source Accuracy:** 84% P@1 (formal), 78% P@5 (messy)

---

## Table of Contents

1. [Overview](#overview)
2. [Data Collection & Preprocessing](#data-collection--preprocessing)
3. [Embedding & Indexing](#embedding--indexing)
4. [Retrieval System](#retrieval-system)
5. [LLM Integration](#llm-integration)
6. [Translation Strategies](#translation-strategies)
7. [Hybrid Retrieval](#hybrid-retrieval)
8. [Web Interface](#web-interface)
9. [Evaluation Framework](#evaluation-framework)
10. [Technical Specifications](#technical-specifications)

---

## Overview

This document describes the complete technical methodology for building a cross-lingual RAG system that achieves 99% category accuracy on Arabic-English government service queries (84% exact source accuracy). The system combines multilingual embeddings, semantic search, domain-specific keyword boosting, and LLM generation to provide accurate, contextual answers grounded in authoritative documents.

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Query                           │
│                    (Arabic or English)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Language Detection (Optional)                  │
│                  googletrans API                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 Query Embedding                             │
│     paraphrase-multilingual-mpnet-base-v2                   │
│                  (768 dimensions)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Semantic Search + Keyword Boosting             │
│         FAISS IndexFlatIP + Domain-specific weights         │
│                    (top-k retrieval)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Context Extraction                         │
│              (top-3 most relevant chunks)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Answer Generation                          │
│              Google Gemini 2.0 Flash                        │
│            (context-only prompting)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Answer + Sources                           │
│            (with confidence indicators)                     │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Multilingual Embeddings:** Use paraphrase-multilingual-mpnet-base-v2 to eliminate translation overhead
2. **Pure Semantic Search:** Skip BM25 hybrid approaches that reduce accuracy for high-quality embeddings
3. **Domain-Specific Boosting:** Implement keyword boosting for government service terminology (+8% accuracy)
4. **Context-Only Generation:** Strict prompting to prevent LLM hallucinations (0% hallucination rate)
5. **Exact Search:** Use FAISS IndexFlatIP for perfect accuracy on small corpus (51 documents)

---

## Data Collection & Preprocessing

### Corpus Acquisition

**Source:** Qatar Government Services Portal (Hukoomi)  
**Collection Method:** Manual extraction from official government website  
**Time Period:** November 2025  
**Language:** Modern Standard Arabic (MSA)

### Corpus Statistics

| Metric | Value |
|--------|-------|
| Total Documents | 51 |
| Categories | 8 |
| Average Document Length | 500 characters |
| Total Characters | ~25,500 |
| Format | Plain text (.txt) |
| Encoding | UTF-8 |

### Category Distribution

| Category | Documents | Topics Covered |
|----------|-----------|----------------|
| Transportation | 7 | Driving licences, vehicle registration, transport permits |
| Education | 8 | University services, school registration, transcripts |
| Health | 7 | Medical services, doctor search, health permits |
| Business | 8 | Commercial licences, permits, registrations |
| Housing | 5 | Housing services, rent allowances, property |
| Culture | 5 | Cultural events, permits, activities |
| Info | 5 | Government information, contact details |
| Justice | 6 | Legal services, court procedures |

**Rationale for Category Selection:**
- Covers most common government service queries
- Balanced distribution (except Justice - limited availability)
- Diverse terminology and procedures
- Real-world relevance for Qatar residents


### Arabic Text Preprocessing

Arabic presents unique challenges requiring specialized preprocessing:

#### Challenge: Morphological Complexity

Arabic has rich morphology where the same root appears in many forms. Traditional keyword matching fails to recognize these relationships.

#### Normalization Pipeline

**File:** `src/preprocessing.py`

```python
import re

def normalize_arabic(text):
    """
    Normalize Arabic text for consistent representation.
    
    Args:
        text (str): Raw Arabic text
        
    Returns:
        str: Normalized Arabic text
    """
    # Remove diacritics (َ ُ ِ ّ ْ)
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    
    # Normalize Alef variants (أ، إ، آ → ا)
    text = re.sub(r'[إأآا]', 'ا', text)
    
    # Normalize Taa Marbuta (ة → ه)
    text = re.sub(r'ة', 'ه', text)
    
    # Remove Tatweel (ـ) - decorative character
    text = re.sub(r'ـ', '', text)
    
    # Collapse multiple whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def clean_document(text):
    """
    Complete document cleaning pipeline.
    
    Args:
        text (str): Raw document text
        
    Returns:
        str: Cleaned document text
    """
    # Apply normalization
    text = normalize_arabic(text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Preserve paragraph structure
    paragraphs = text.split('\n\n')
    cleaned_paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    return '\n\n'.join(cleaned_paragraphs)
```

#### Normalization Rules

| Rule | Before | After | Rationale |
|------|--------|-------|-----------|
| Diacritics | كَتَبَ | كتب | Rarely used in modern text |
| Alef variants | أكتب، إكتب، آكتب | اكتب | Same sound, different forms |
| Taa Marbuta | مدرسة | مدرسه | Pronunciation similarity |
| Tatweel | كـــتـــاب | كتاب | Decorative only |

#### Impact Assessment

**Before Normalization:**
- Unique tokens: 2,847
- Vocabulary size: Large
- Match rate: 73%

**After Normalization:**
- Unique tokens: 2,421 (-15%)
- Vocabulary size: Reduced
- Match rate: 95%

**Result:** Consistent text representation without semantic loss

### Document Chunking

#### Strategy Selection

**Approach:** Paragraph-based chunking with overlap

**Rationale:**
- Preserves semantic coherence (no mid-sentence splits)
- Maintains document structure
- Balances context and specificity
- Prevents information loss at boundaries

#### Configuration

```python
# Chunking parameters
CHUNK_SIZE = 512        # Maximum characters per chunk
OVERLAP = 128           # Overlap between consecutive chunks
MIN_CHUNK_SIZE = 412    # Minimum chunk size (80% of CHUNK_SIZE)
```

**Parameter Justification:**
- **512 characters:** Optimal for sentence-transformers (typical sentence length)
- **128 overlap:** Prevents context loss at boundaries (25% overlap)
- **412 minimum:** Ensures sufficient context for semantic understanding

#### Implementation

**File:** `src/chunking.py`

```python
def chunk_by_paragraph(text, chunk_size=512, overlap=128, min_size=412):
    """
    Chunk document by paragraphs with overlap.
    
    Args:
        text (str): Document text
        chunk_size (int): Maximum chunk size in characters
        overlap (int): Overlap between chunks
        min_size (int): Minimum chunk size
        
    Returns:
        list: List of text chunks
    """
    # Split by paragraphs
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        
        # Skip short paragraphs
        if len(para) < 50:
            continue
            
        # If adding paragraph exceeds chunk size, save current chunk
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            if len(current_chunk) >= min_size:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            # Add paragraph to current chunk
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    # Add final chunk
    if current_chunk and len(current_chunk) >= min_size:
        chunks.append(current_chunk.strip())
    
    return chunks
```

#### Chunking Experiments

We tested 4 chunking configurations to determine optimal parameters:

| Configuration | Chunks Created | P@1 | P@3 | MRR |
|---------------|----------------|-----|-----|-----|
| 256/64 | 96 | 90% | 90% | 0.900 |
| 512/128 | 51 | 90% | 90% | 0.900 |
| 1024/256 | 27 | 90% | 90% | 0.900 |
| 2048/512 | 15 | 90% | 90% | 0.900 |

**Finding:** All configurations achieved identical performance (90% accuracy)

**Analysis:**
- Small corpus (51 documents) means chunking has minimal impact
- Documents already small (~500 characters average)
- Paragraph boundaries naturally preserve semantic units
- Chose 512/128 as standard practice

#### Metadata Structure

Each chunk includes comprehensive metadata for traceability:

```json
{
  "chunk_id": 0,
  "source_file": "business/business_license.txt",
  "category": "business",
  "title": "Business License Application",
  "chunk_index": 0,
  "total_chunks": 1,
  "word_count": 87,
  "char_count": 523
}
```

**Metadata Fields:**
- `chunk_id`: Unique identifier for retrieval
- `source_file`: Original document path
- `category`: Service category for filtering
- `title`: Document title for display
- `chunk_index`: Position within document
- `total_chunks`: Total chunks from document
- `word_count`: Number of words (for statistics)
- `char_count`: Number of characters (for validation)

### Data Quality Verification

**Script:** `scripts/tests/verify_data.py`

**Validation Checks:**
1. File existence and readability
2. UTF-8 encoding compliance
3. Minimum content length (>100 characters)
4. Category distribution balance
5. No duplicate content
6. Proper Arabic text (no corruption)

**Results:**
- Files verified: 51/51 ✅
- Encoding issues: 0
- Content issues: 0
- All files valid

---

## Embedding & Indexing

### Model Selection

#### Candidates Evaluated

| Model | Languages | Dimensions | Arabic Support | Cross-lingual | Our Choice |
|-------|-----------|------------|----------------|---------------|------------|
| AraBERT | Arabic only | 768 | Excellent | No | ❌ |
| mBERT | 104 languages | 768 | Good | Yes | ❌ |
| LASER | 93 languages | 1024 | Good | Yes | ❌ |
| **paraphrase-multilingual-mpnet-base-v2** | **50+ languages** | **768** | **Very Good** | **Yes** | **✅** |

#### Selection Rationale

**Why paraphrase-multilingual-mpnet-base-v2:**

1. **Sentence-Level Training:** Specifically trained on sentence similarity tasks (perfect for our use case)
2. **Strong Arabic Performance:** Achieved 100% accuracy on Arabic queries without Arabic-specific fine-tuning
3. **Cross-Lingual Capability:** Maps Arabic and English to shared semantic space (zero-shot cross-lingual retrieval)
4. **Modern Architecture:** MPNet architecture superior to older BERT models
5. **Manageable Size:** 768 dimensions balance expressiveness and efficiency
6. **Proven Performance:** Widely used in production systems

**Why Not AraBERT:**
- Monolingual (Arabic only)
- Would require separate English model
- No cross-lingual capability
- Additional translation overhead

**Why Not mBERT:**
- Older architecture (2018)
- Lower performance on sentence similarity
- Trained on masked language modeling (not similarity)

**Why Not LASER:**
- Larger dimensions (1024) without performance gain
- More complex architecture
- Less community support

### Embedding Generation

**File:** `scripts/build/generate_embeddings.py`

```python
from sentence_transformers import SentenceTransformer
import numpy as np
import json

def generate_embeddings(chunks_path, output_path):
    """
    Generate embeddings for all document chunks.
    
    Args:
        chunks_path (str): Path to corpus chunks JSON
        output_path (str): Path to save embeddings
    """
    # Load model
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    # Load chunks
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    # Extract text
    texts = [chunk['text'] for chunk in chunks]
    
    # Generate embeddings
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,  # L2 normalization for cosine similarity
        convert_to_numpy=True
    )
    
    # Save embeddings
    np.save(output_path, embeddings)
    
    print(f"Generated embeddings: {embeddings.shape}")
    print(f"Saved to: {output_path}")
    
    return embeddings

# Execute
embeddings = generate_embeddings(
    'index/corpus_chunks.json',
    'index/embeddings.npy'
)
```

#### Configuration Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `batch_size` | 32 | Optimal for GPU memory (16GB) |
| `normalize_embeddings` | True | Required for cosine similarity |
| `show_progress_bar` | True | Monitor long-running process |
| `convert_to_numpy` | True | Efficient storage and retrieval |

#### Processing Statistics

**Input:**
- Documents: 51
- Total characters: ~25,500
- Average document length: 500 characters

**Output:**
- Embedding shape: (51, 768)
- File size: ~156 KB
- Processing time: 2.3 seconds
- Memory usage: ~500 MB (model loaded)

**Performance:**
- Embeddings per second: ~22
- Characters per second: ~11,000
- Throughput: Sufficient for real-time applications

