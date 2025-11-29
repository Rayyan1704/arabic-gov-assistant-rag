# Quick Start Guide

**Setup and Testing Instructions**

---

## Prerequisites

- Python 3.12+
- Virtual environment activated
- `.env` file with `GEMINI_API_KEY`

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Testing

### System Verification
```bash
python show_system_summary.py
```
Output: System overview with metrics

### Production System Test
```bash
python test_production_system.py
```
Output: Critical query validation results

### Comprehensive Evaluation
```bash
python test_comprehensive_100_queries.py
```
Output: 100-query test results with accuracy metrics

### Final Accuracy Test
```bash
python test_final_accuracy.py
```
Output: Accuracy measurement on test set

---

## Usage

### Python API
```python
from sentence_transformers import SentenceTransformer
from src.retrieval import RetrieverSystem
from src.llm_generator import AnswerGenerator

# Initialize
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
retriever = RetrieverSystem(
    'index/embeddings.npy',
    'index/corpus_chunks.json',
    'index/corpus_meta.json'
)
generator = AnswerGenerator()

# Query
query = "كيف أحصل على رخصة قيادة؟"
query_emb = model.encode([query])[0]

# Retrieve
results = retriever.search(query_emb, k=3, query_text=query)

# Generate answer
answer = generator.generate_answer(query, [r['chunk'] for r in results])
print(answer)
```

### Web Interface
```bash
streamlit run app.py
```

### Command Line
```bash
python test_production_system.py
python test_comprehensive_100_queries.py
```

---

## Expected Performance

### Metrics
- Accuracy: 96.0% (96/100 queries)
- Response Time: 0.16s average
- Statistical Significance: p < 0.0001

### Output Format
```
Query: كيف أحصل على رخصة قيادة؟
Retrieved: 3 documents
Top score: 0.847

Answer: [Generated response]
Sources: [transportation/doc1.txt, transportation/doc2.txt]
```

---

## Configuration

### Retrieval Parameters
```python
results = retriever.search(
    query_emb,
    k=10,              # Number of results
    query_text=query   # Enable keyword boosting
)
```

### LLM Parameters
```python
# In src/llm_generator.py
generation_config=genai.types.GenerationConfig(
    temperature=0.1,
    max_output_tokens=1000
)
```

---

## Key Files

### Source Code
- `src/retrieval.py` - FAISS retrieval with enhancements
- `src/llm_generator.py` - LLM generation
- `src/category_retrieval.py` - Category-aware retrieval
- `src/chunking.py` - Document chunking
- `src/preprocessing.py` - Text preprocessing

### Test Scripts
- `test_production_system.py` - Critical query validation
- `test_comprehensive_100_queries.py` - Large-scale testing
- `test_final_accuracy.py` - Accuracy measurement
- `verify_data.py` - Data quality check

### Documentation
- `RESEARCH_SUMMARY.md` - Research findings
- `PROJECT_COMPLETE.md` - Project summary
- `README.md` - Project overview
- `QUICK_START_GUIDE.md` - This file

---

## Troubleshooting

### GEMINI_API_KEY not found
Create `.env` file:
```
GEMINI_API_KEY=your_key_here
```

### Module not found
Install dependencies:
```bash
pip install -r requirements.txt
```

### Index files not found
Build index:
```bash
python build_retrieval_system.py
```

---

## System Reference

### Statistics
- Documents: 51
- Categories: 8
- Embedding dimensions: 768
- Accuracy: 96.0%
- Response time: 0.16s

### Commands
```bash
# System summary
python show_system_summary.py

# Production test
python test_production_system.py

# Comprehensive evaluation
python test_comprehensive_100_queries.py

# Accuracy measurement
python test_final_accuracy.py

# Run all experiments
python run_all_experiments.py
```

---

## Verification Checklist

- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] `show_system_summary.py` executes
- [ ] `test_production_system.py` passes
- [ ] System architecture understood

---

For detailed information:
- `RESEARCH_SUMMARY.md` - Research findings
- `PROJECT_COMPLETE.md` - Project summary
- `README.md` - Project overview
