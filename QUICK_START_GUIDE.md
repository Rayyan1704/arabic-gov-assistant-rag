# 🚀 Quick Start Guide - AraGovAssist RAG System

**5-Minute Setup & Testing Guide**

---

## ⚡ Prerequisites

```bash
# Python 3.8+
# Virtual environment activated
# .env file with GEMINI_API_KEY
```

---

## 📦 Installation (1 minute)

```bash
# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Quick Tests (4 minutes)

### 1. Verify System (30 seconds)
```bash
python show_system_summary.py
```
**Expected:** Complete system overview with all metrics

### 2. Test Basic RAG (1 minute)
```bash
python test_end_to_end.py
```
**Expected:** 5 queries answered with 90% accuracy

### 3. Test Advanced Retrieval (2 minutes)
```bash
python test_reranked_end_to_end.py
```
**Expected:** 5 queries with reranking, improved relevance scores

### 4. Compare Approaches (30 seconds)
```bash
python test_category_reranking.py
```
**Expected:** Comparison of global, category, and reranked search

---

## 🎯 Usage Examples

### Python API
```python
from src.category_retrieval import RerankedRetriever
from src.llm_generator import AnswerGenerator
from sentence_transformers import SentenceTransformer

# Initialize
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
retriever = RerankedRetriever(
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)
generator = AnswerGenerator()

# Query
query = "كيف أحصل على بطاقة صحية؟"
query_emb = model.encode([query])[0]

# Retrieve with reranking
docs = retriever.search_with_rerank(query, query_emb, final_k=3)

# Generate answer
result = generator.generate_answer(query, docs)
print(result['answer'])
```

### Command Line (Simple)
```bash
# Run any test script
python test_10_queries.py
python chunking_experiments.py
```

---

## 📊 What to Expect

### Performance
- **Accuracy:** 90% (9/10 queries correct)
- **Response Time:** 3-5 seconds
- **Reranking Improvement:** +1575% better scores
- **Category Detection:** 100% accurate

### Output Format
```
Query: كيف أحصل على بطاقة صحية؟
Detected category: health
Retrieved: 3 documents
Top score: 8.506 (reranked)

Answer: [Gemini-generated response]
Sources: [health/doc1.txt, health/doc2.txt]
```

---

## 🔧 Configuration

### Change Retrieval Settings
```python
# In your code
retriever.search_with_rerank(
    query, 
    query_emb,
    initial_k=20,  # Candidates to retrieve
    final_k=5      # Results after reranking
)
```

### Change LLM Settings
```python
# In src/llm_generator.py
generation_config=genai.types.GenerationConfig(
    temperature=0.3,      # Lower = more factual
    max_output_tokens=500 # Response length
)
```

---

## 📁 Key Files

### Source Code
- `src/category_retrieval.py` - Advanced retrieval ⭐
- `src/llm_generator.py` - LLM generation
- `src/retrieval.py` - Basic retrieval
- `src/chunking.py` - Document chunking
- `src/preprocessing.py` - Text preprocessing

### Test Scripts
- `test_reranked_end_to_end.py` - Full pipeline ⭐
- `test_category_reranking.py` - Compare approaches ⭐
- `test_10_queries.py` - Accuracy test
- `test_end_to_end.py` - Basic pipeline

### Documentation
- `FINAL_COMPLETE_STATUS.md` - Complete overview ⭐
- `DAY5_CHECKPOINT.md` - Advanced features ⭐
- `README.md` - Project README
- `QUICK_START_GUIDE.md` - This file

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Create `.env` file with:
```
GEMINI_API_KEY=your_key_here
```

### Issue: "Module not found"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Index files not found"
**Solution:** Index files should already exist in `index/` folder. If missing:
```bash
python build_retrieval_system.py
```

### Issue: Slow performance
**Solution:** Normal! Reranking takes 1-2 seconds. To speed up:
- Reduce `initial_k` (fewer candidates)
- Skip reranking (use basic retrieval)

---

## 📈 Performance Tuning

### For Speed (< 2 seconds)
```python
# Use basic retrieval without reranking
from src.retrieval import FAISSRetriever
retriever = FAISSRetriever('index/faiss.index', ...)
results = retriever.search(query_emb, k=3)
```

### For Accuracy (current setup)
```python
# Use reranking (current default)
retriever = RerankedRetriever(...)
results = retriever.search_with_rerank(query, query_emb)
```

### For Scale (1000+ docs)
```python
# Use category-specific search
category = retriever.detect_category(query)
results = retriever.search(query_emb, category=category)
```

---

## 🎓 Learning Path

### Beginner
1. Run `test_end_to_end.py` - See basic RAG
2. Read `DAY1_CHECKPOINT.md` - Understand data
3. Read `DAY2_CHECKPOINT.md` - Understand embeddings

### Intermediate
1. Run `test_category_reranking.py` - Compare approaches
2. Read `DAY4_CHECKPOINT.md` - Understand experiments
3. Read `DAY5_CHECKPOINT.md` - Understand reranking

### Advanced
1. Read `FINAL_COMPLETE_STATUS.md` - Full system
2. Modify `src/category_retrieval.py` - Customize
3. Deploy with FastAPI - Production use

---

## 🚀 Next Steps

### Option 1: Deploy
```bash
# Create FastAPI wrapper
# Add Docker container
# Deploy to cloud
```

### Option 2: Enhance
```bash
# Add Streamlit UI
# Expand document corpus
# Add hybrid search (BM25)
```

### Option 3: Portfolio
```bash
# Push to GitHub
# Write blog post
# Present findings
```

---

## 📞 Quick Reference

### System Stats
- Documents: 50
- Categories: 8
- Chunks: 50
- Embedding dim: 768
- Accuracy: 90%
- Response time: 3-5s

### Key Commands
```bash
# Show summary
python show_system_summary.py

# Test basic RAG
python test_end_to_end.py

# Test advanced RAG
python test_reranked_end_to_end.py

# Compare approaches
python test_category_reranking.py

# Run experiments
python test_10_queries.py
python chunking_experiments.py
```

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] `show_system_summary.py` runs successfully
- [ ] `test_end_to_end.py` shows 90% accuracy
- [ ] `test_reranked_end_to_end.py` shows reranking
- [ ] Understand the system architecture
- [ ] Ready to deploy or enhance!

---

**You're all set! 🎉**

For detailed information, see:
- `FINAL_COMPLETE_STATUS.md` - Complete system overview
- `DAY5_CHECKPOINT.md` - Advanced features
- `README.md` - Project documentation
