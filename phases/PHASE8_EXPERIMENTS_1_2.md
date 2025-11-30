# Phase 8: Research Experiments 1-2

**Timeline:** Days 15-16 (8 hours)  
**Focus:** Translation Strategies and Hybrid Retrieval Experiments  
**Status:** Complete

---

## Research Objectives

**Primary Question:** What retrieval strategies optimize accuracy for cross-lingual Arabic-English RAG systems?

**Sub-Questions:**
1. How do translation strategies affect retrieval accuracy for English queries?
2. Does hybrid retrieval (semantic + keyword) improve performance over pure semantic search?

---

## Experiment 1: Translation Strategies

### Methodology
**File:** `experiments/experiment1_translation_strategies.py`

**Methods Tested:**
1. Direct English embeddings (no translation)
2. Multilingual embeddings
3. Translation + Arabic embeddings
4. Back-translation query expansion

**Test Set:** 12 English queries, 4 categories

**Metrics:** Precision@1, P@3, P@5, MRR, response time

### Results

| Method | P@1 | P@3 | MRR | Time (s) |
|--------|-----|-----|-----|----------|
| Direct English | 100% | 100% | 1.000 | 0.13 |
| Multilingual | 100% | 100% | 1.000 | 0.11 |
| Translate + Embed | 83.3% | 83.3% | 0.833 | 0.34 |
| Back-translation | 83.3% | 91.7% | 0.861 | 1.14 |

### Analysis
- Multilingual embeddings achieved 100% accuracy on English queries without translation
- Translation increased latency from 0.11s to 0.34s without accuracy improvement
- Back-translation showed no measurable improvement over direct translation

**Output:** `index/experiment1_translation_strategies.json`

---

## Experiment 2: Hybrid Retrieval

### Methodology
**File:** `experiments/experiment2_hybrid_retrieval.py`

**Methods Tested:**
1. Semantic only (baseline)
2. BM25 only
3. Weighted hybrid (70% semantic, 30% BM25)
4. Weighted hybrid (50% semantic, 50% BM25)
5. Cascade (BM25 first-stage, semantic reranking)

**Test Set:** 50 Arabic queries, 8 categories

**Metrics:** Precision@1, P@3, P@5, MRR, response time

### Results

| Method | P@1 | P@3 | P@5 | MRR | Time (s) |
|--------|-----|-----|-----|-----|----------|
| Semantic Only | 84% | 86% | 86% | 0.852 | 0.14 |
| BM25 Only | 56% | 70% | 76% | 0.638 | 0.0003 |
| Hybrid 70/30 | 80% | 86% | 88% | 0.837 | 0.10 |
| Hybrid 50/50 | 70% | 82% | 86% | 0.771 | 0.11 |
| Cascade | 84% | 86% | 86% | 0.852 | 0.11 |

### Analysis
- Pure semantic search achieved 84% P@1
- BM25 hybrid approaches reduced accuracy to 80% and 70% P@1
- Cascade approach matched semantic accuracy (84%) with 0.03s latency reduction

**Output:** `index/experiment2_hybrid_retrieval.json`

---

## Implementation Details

### Translation Strategies

**Method 1: Direct English**
```python
query_emb = model.encode([english_query])
```

**Method 2: Multilingual**
```python
query_emb = model.encode([english_query])  # Same as Method 1
```

**Method 3: Translate + Embed**
```python
arabic_query = translator.translate(english_query)
query_emb = model.encode([arabic_query])
```

**Method 4: Back-translation**
```python
ar1 = translate_to_arabic(english_query)
en_back = translate_to_english(ar1)
ar2 = translate_to_arabic(en_back)
query_emb = (embed(ar1) + embed(ar2)) / 2
```

### Hybrid Retrieval

**Weighted Combination:**
```python
semantic_score = cosine_similarity(query_emb, doc_emb)
bm25_score = bm25.get_scores(query_tokens)
final_score = α * semantic_score + (1-α) * bm25_score
```

**Cascade Approach:**
```python
# Stage 1: BM25 retrieval (50 candidates)
candidates = bm25.get_top_k(query, k=50)
# Stage 2: Semantic reranking
reranked = semantic_rerank(query, candidates, k=10)
```

---

## Results Summary

### Translation Strategy
The paraphrase-multilingual-mpnet-base-v2 model processed English queries without translation, achieving 100% accuracy. Translation added 0.23s latency without accuracy improvement.

### Hybrid Retrieval
Pure semantic search achieved 84% P@1. BM25 hybrid configurations reduced accuracy to 70-80% P@1. Cascade approach maintained 84% accuracy with 0.03s latency reduction.

---

## Files Generated

- `experiments/experiment1_translation_strategies.py`
- `experiments/experiment2_hybrid_retrieval.py`
- `index/experiment1_translation_strategies.json`
- `index/experiment2_hybrid_retrieval.json`
- `run_all_experiments.py` (master script)

---

## Challenges and Solutions

### Challenge 1: Experiment Design
**Issue:** Uncertain how to structure systematic experiments  
**Cause:** First time conducting ML experiments  
**Solution:** Researched RAG evaluation methods, designed controlled comparisons

### Challenge 2: Back-Translation Implementation
**Issue:** Complex logic for query expansion  
**Cause:** Multiple translation steps  
**Solution:** Simplified to: EN→AR→EN→AR, averaged embeddings

### Challenge 3: BM25 Integration
**Issue:** BM25 library (rank-bm25) not working with Arabic  
**Cause:** Tokenization issues  
**Solution:** Implemented custom Arabic tokenizer, integrated with BM25

### Challenge 4: Score Normalization
**Issue:** BM25 and semantic scores on different scales  
**Cause:** Different algorithms  
**Solution:** Normalized both to [0,1] range before combining

### Challenge 5: Unexpected Hybrid Results
**Issue:** Hybrid search performed worse than semantic-only  
**Cause:** High-quality embeddings already optimal  
**Solution:** Documented finding, validated with multiple test sets

### Challenge 6: Statistical Significance
**Issue:** Small test set (12 queries) for Experiment 1  
**Cause:** Time constraints  
**Solution:** Noted limitation, planned larger evaluation in Experiment 3

---

## Time Breakdown

- Experiment 1 design: 1 hour
- Experiment 1 implementation: 1.5 hours
- Experiment 1 analysis: 0.5 hours
- Experiment 2 design: 1 hour
- Experiment 2 implementation: 2 hours
- Experiment 2 analysis: 1 hour
- Documentation: 1 hour

**Total:** 8 hours (Days 15-16)

---

## Next Phase

Phase 9: Comprehensive evaluation and ablation study (Days 17-18)
