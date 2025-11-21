# Day 2: Embeddings & Retrieval

## Overview
Generate vector embeddings and build FAISS index for semantic search.

## Tasks

### Morning Session (4 hours)

#### Task 1: Understanding Embeddings (1 hour)
**Concepts:**
- Embeddings convert text into vectors (lists of numbers)
- Similar meaning = similar vectors
- Vector similarity measured by cosine similarity

**Why embeddings?**
- Can't search text directly at scale
- Embeddings capture semantic meaning
- "سيارة" and "مركبة" have similar embeddings (both mean vehicle)

**Model:** `paraphrase-multilingual-mpnet-base-v2`
- 768-dimensional vectors
- Trained on 50+ languages including Arabic

**Run:** `02_embeddings.ipynb` - Step 1

#### Task 2: Generate Embeddings (2 hours)
**What it does:**
- Loads preprocessed chunks from Day 1
- Generates embeddings for all 34 chunks
- Saves to `index/embeddings.npy`

**Run:** `02_embeddings.ipynb` - Steps 2-4

**Expected output:**
- Embeddings shape: (34, 768)
- File size: ~200KB

#### Task 3: Verify Quality (1 hour)
**Test queries matching your data:**
- "كيف أحصل على رخصة ليموزين؟" → transportation/limo_license
- "ما هي خطوات تسجيل المقررات؟" → education/course_registration
- "كيف أطلب استشارة طبية؟" → health/doctor_consultation

**Run:** `02_embeddings.ipynb` - Steps 5-6

**Verify:**
- Do top matches make sense?
- Are scores reasonable (0.3-0.8 range)?
- Do categories match query intent?

### Evening Session (4 hours)

#### Task 4: Learn FAISS (1 hour)
**What is FAISS?**
- Facebook AI Similarity Search
- Finds nearest neighbors super fast
- Essential for large-scale retrieval

**Index types:**
- `IndexFlatIP` - Exact search with inner product (cosine similarity)
- We use this for small datasets (<100K vectors)

**Key concepts:**
- k: number of neighbors to return (we use k=10)
- Cosine similarity: Dot product of normalized vectors (larger = more similar)

#### Task 5: Build FAISS Index (1.5 hours)
**What it does:**
- Creates `RetrieverSystem` class
- Builds FAISS index from embeddings
- Saves to `index/faiss.index`

**Run:** `03_retrieval_testing.ipynb` - Steps 1-2

**Expected output:**
- Index with 34 vectors
- File size: ~200KB

#### Task 6: Test Retrieval (1.5 hours)
**Test queries:**
```python
test_queries = [
    "كيف أحصل على رخصة ليموزين في قطر؟",
    "ما هي إجراءات تسجيل المقررات في جامعة قطر؟",
    "كيف أطلب استشارة طبية؟",
    "ما هي متطلبات تقديم العروض للمناقصات؟",
]
```

**Run:** `03_retrieval_testing.ipynb` - Steps 3-4

**Evaluate:**
- Are top-3 results relevant?
- What's the typical score range?
- Do categories match query intent?

## Checkpoint

At end of Day 2, you should have:
- ✅ `index/embeddings.npy` - Vector embeddings
- ✅ `index/faiss.index` - FAISS index
- ✅ `src/retrieval.py` - Retrieval system
- ✅ Verified retrieval quality

## Troubleshooting

### Low retrieval scores (<0.3)
- Check if preprocessing is too aggressive
- Verify chunks contain enough context
- Try different embedding model

### Wrong category retrieved
- Add category-specific keywords to chunks
- Use category filtering in retrieval
- Improve query preprocessing

### Slow retrieval
- FAISS should be fast (<1ms for 34 vectors)
- If slow, check if index is loaded correctly
- Verify embeddings are normalized

## Next Steps

Day 3: LLM Integration
- Setup Gemini API
- Build RAG pipeline
- Generate natural language answers
