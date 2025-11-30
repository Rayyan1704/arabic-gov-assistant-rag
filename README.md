# Arabic Government Services RAG System

A cross-lingual Retrieval-Augmented Generation system for Qatar government services with 96% accuracy on bilingual queries.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)](https://streamlit.io)
[![FAISS](https://img.shields.io/badge/FAISS-1.7.4-green.svg)](https://faiss.ai)

---

## Overview

**Objective:** Enable cross-lingual information retrieval for Qatar government services.

**System Capabilities:**
- Searches 51 government service documents across 8 categories
- Processes Arabic and English queries with 96% accuracy
- Generates contextual answers using Google Gemini 2.0 Flash
- Responds in 0.16s average time
- Provides web-based interface via Streamlit

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Overall Accuracy | 96.0% (96/100 queries) |
| Arabic Accuracy | 96.0% (48/50) |
| English Accuracy | 96.0% (48/50) |
| Response Time | 0.16s average |
| Statistical Significance | p < 0.0001 |
| Improvement over BM25 | +40 percentage points (71% relative) |

---

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/Rayyan1704/arabic-gov-assistant-rag.git
cd arabic-gov-assistant-rag

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Build System

```bash
# Step 1: Process documents into chunks
python scripts/build/process_all_documents.py

# Step 2: Generate embeddings
python scripts/build/generate_embeddings.py

# Step 3: Build FAISS index
python scripts/build/build_retrieval_system.py
```

### 4. Run Application

```bash
# Web interface
streamlit run app.py

# Or run experiments
python run_all_experiments.py
```

---

## Project Structure

```
arabic-gov-assistant-rag/
│
├── app.py                          # Streamlit web interface
├── run_all_experiments.py          # Master experiment script
│
├── src/                            # Core modules (7 files)
│   ├── preprocessing.py            # Arabic text normalization
│   ├── chunking.py                 # Document chunking
│   ├── retrieval.py                # FAISS retrieval + enhancements
│   ├── category_retrieval.py       # Category-aware retrieval
│   ├── llm_generator.py            # Gemini LLM integration
│   ├── translator.py               # Google Translate integration
│   └── __init__.py
│
├── scripts/                        # Build and test scripts
│   ├── build/                      # Build pipeline (3 scripts)
│   │   ├── process_all_documents.py
│   │   ├── generate_embeddings.py
│   │   └── build_retrieval_system.py
│   ├── tests/                      # Test scripts (2 scripts)
│   │   ├── verify_data.py
│   │   └── test_comprehensive_100_queries.py
│   └── README.md
│
├── data/                           # Document corpus (51 docs, 8 categories)
│   ├── business/
│   ├── culture/
│   ├── education/
│   ├── health/
│   ├── housing/
│   ├── info/
│   ├── justice/
│   └── transportation/
│
├── experiments/                    # Research experiments (4 experiments)
│   ├── experiment1_translation_strategies.py
│   ├── experiment2_hybrid_retrieval.py
│   ├── experiment3_comprehensive_evaluation.py
│   ├── experiment4_ablation_study.py
│   └── test_queries_dataset.json
│
├── index/                          # Generated indexes and results
│   ├── embeddings.npy
│   ├── faiss.index
│   ├── corpus_chunks.json
│   ├── corpus_meta.json
│   └── experiment*.json
│
├── notebooks/                      # Jupyter notebooks (2 notebooks)
│   ├── 01_data_exploration.ipynb
│   └── 02_embeddings.ipynb
│
├── phases/                         # Phase documentation (10 files)
│   ├── PHASE1_SETUP_AND_DATA.md
│   ├── PHASE2_CORE_SYSTEM.md
│   ├── PHASE3_EMBEDDINGS.md
│   ├── PHASE4_RETRIEVAL.md
│   ├── PHASE5_RERANKING.md
│   ├── PHASE6_UI_DEVELOPMENT.md
│   ├── PHASE7_OPTIMIZATION.md
│   ├── PHASE8_EXPERIMENTS_1_2.md
│   ├── PHASE9_EXPERIMENTS_3_4.md
│   └── PHASE10_FINALIZATION.md
│
└── Documentation/                  # Research documentation (5 files)
    ├── README.md                   # This file
    ├── QUICK_START_GUIDE.md        # Setup instructions
    ├── RESEARCH_SUMMARY.md         # Research findings
    ├── PROJECT_TIMELINE.md         # 20-day development plan
    └── PROJECT_COMPLETE.md         # Completion summary
```

---

## System Architecture

### Processing Pipeline

```
User Query (Arabic/English)
    ↓
Language Detection
    ↓
Translation (if English)
    ↓
Query Embedding (768-dim)
    ↓
FAISS Similarity Search
    ↓
Keyword Boosting
    ↓
Top-k Selection
    ↓
LLM Answer Generation (Gemini)
    ↓
Response with Sources
```

### Technology Stack

- **Embeddings:** paraphrase-multilingual-mpnet-base-v2
- **Vector Index:** FAISS IndexFlatIP
- **LLM:** Google Gemini 2.0 Flash
- **Translation:** Google Translate API
- **UI:** Streamlit
- **Language:** Python 3.12

---

## Research Experiments

### Experiment 1: Translation Strategies
**Test Set:** 12 English queries

**Results:**
- Multilingual embeddings: 100% accuracy without translation
- Translation overhead: +0.23s latency
- **Finding:** Modern multilingual models eliminate translation requirement

### Experiment 2: Hybrid Retrieval
**Test Set:** 50 Arabic queries

**Results:**
- Pure semantic: 84% P@1
- BM25 hybrid: 70-80% P@1
- **Finding:** High-quality embeddings outperform hybrid approaches

### Experiment 3: Comprehensive Evaluation
**Test Set:** 100 queries (50 Arabic + 50 English)

**Results:**
- Overall accuracy: 96.0%
- Statistical significance: p < 0.0001
- **Finding:** System validated at scale with equal cross-lingual performance

### Experiment 4: Ablation Study
**Test Set:** 100 queries

**Results:**
- Keyword boosting: +7% contribution
- Translation: +10% for English queries
- Title matching: 0% impact
- **Finding:** Keyword boosting critical for domain-specific retrieval

---

## Key Features

### Technical Highlights
- Cross-lingual query processing (Arabic/English)
- Keyword boosting for domain-specific terms
- Statistical validation (p < 0.0001)
- Zero hallucination (context-only responses)
- Production-ready web interface

### Research Contributions
1. Systematic comparison of translation strategies for Arabic RAG
2. Evaluation of hybrid retrieval approaches
3. Quantification of component contributions via ablation study
4. 100-query bilingual benchmark dataset

---

## Usage Examples

### Web Interface
```bash
streamlit run app.py
```

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
results = retriever.search(query_emb, k=3, query_text=query)
answer = generator.generate_answer(query, [r['chunk'] for r in results])
```

### Run Tests
```bash
# Verify data quality
python scripts/tests/verify_data.py

# Run comprehensive evaluation
python scripts/tests/test_comprehensive_100_queries.py

# Run all experiments
python run_all_experiments.py
```

---

## Development Timeline

**Duration:** 20 days (November 19-28, 2025)  
**Total Hours:** ~100 hours

| Phase | Days | Focus |
|-------|------|-------|
| Phase 1-2 | 1-4 | Setup, data collection, embeddings |
| Phase 3-4 | 5-8 | LLM integration, testing |
| Phase 5-6 | 9-12 | Advanced retrieval, UI |
| Phase 7 | 13-14 | Translation, optimization |
| Phase 8-9 | 15-18 | Research experiments |
| Phase 10 | 19-20 | Finalization |

See [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md) for detailed breakdown.

---

## Documentation

### Getting Started
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Setup and usage instructions
- [scripts/README.md](scripts/README.md) - Build pipeline documentation

### Research Documentation
- [RESEARCH_SUMMARY.md](RESEARCH_SUMMARY.md) - Key findings and contributions
- [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) - Project completion summary
- [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md) - Development timeline

### Phase Documentation
- [PHASE1_SETUP_AND_DATA.md](phases/PHASE1_SETUP_AND_DATA.md) - Days 1-2
- [PHASE2_CORE_SYSTEM.md](phases/PHASE2_CORE_SYSTEM.md) - Days 3-4
- [PHASE3_EMBEDDINGS.md](phases/PHASE3_EMBEDDINGS.md) - Days 5-6
- [PHASE4_RETRIEVAL.md](phases/PHASE4_RETRIEVAL.md) - Days 7-8
- [PHASE5_RERANKING.md](phases/PHASE5_RERANKING.md) - Days 9-10
- [PHASE6_UI_DEVELOPMENT.md](phases/PHASE6_UI_DEVELOPMENT.md) - Days 11-12
- [PHASE7_OPTIMIZATION.md](phases/PHASE7_OPTIMIZATION.md) - Days 13-14
- [PHASE8_EXPERIMENTS_1_2.md](phases/PHASE8_EXPERIMENTS_1_2.md) - Days 15-16
- [PHASE9_EXPERIMENTS_3_4.md](phases/PHASE9_EXPERIMENTS_3_4.md) - Days 17-18
- [PHASE10_FINALIZATION.md](phases/PHASE10_FINALIZATION.md) - Days 19-20

---

## Limitations

### Current Limitations
- Justice category: 50% accuracy (limited training data: 4 documents)
- Test set: 100 queries (moderate scale)
- Single domain: Qatar government services
- Languages: Arabic and English only

### Future Work
1. Expand justice category documents (4 → 15+)
2. Add domain-specific legal embeddings
3. Increase test set size (100 → 500+ queries)
4. Evaluate on additional domains
5. Conduct user studies

---

## Citation

If you use this work, please cite:

```bibtex
@misc{arabic-gov-rag-2025,
  title={Cross-Lingual RAG System for Arabic Government Services},
  author={Rayyan},
  year={2025},
  url={https://github.com/Rayyan1704/arabic-gov-assistant-rag}
}
```

---

## License

Educational and research purposes.

---

## Contact

For questions or collaboration:
- GitHub: [@Rayyan1704](https://github.com/Rayyan1704)
- Repository: [arabic-gov-assistant-rag](https://github.com/Rayyan1704/arabic-gov-assistant-rag)
