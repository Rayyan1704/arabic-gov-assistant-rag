# 🇶🇦 AraGovAssist - Qatar Government Services RAG System

A production-grade Retrieval-Augmented Generation (RAG) system for Qatar government services documentation in Arabic, featuring advanced retrieval techniques including cross-encoder reranking and per-category indexes.

## 🎯 System Performance

- **Retrieval Accuracy:** 90% (9/10 test queries)
- **Category Detection:** 100% (5/5 queries)
- **Hallucination Rate:** 0% (honest "I don't know" responses)
- **Response Time:** ~3-5 seconds
- **Reranking Improvement:** Significant (8.759 vs 0.523 scores)

## 📁 Project Structure

```
arabic-gov-assistant-rag/
├── data/                   # Government service documents (50 files)
│   ├── health/            # 7 documents
│   ├── education/         # 8 documents
│   ├── business/          # 8 documents
│   ├── transportation/    # 6 documents
│   ├── justice/           # 6 documents
│   ├── housing/           # 5 documents
│   ├── culture/           # 5 documents
│   └── info/              # 5 documents
├── notebooks/             # Jupyter notebooks for experiments
│   ├── 01_data_exploration.ipynb
│   ├── 02_chunking_experiments.ipynb
│   └── 03_retrieval_testing.ipynb
├── src/                   # Source code
│   ├── __init__.py
│   ├── preprocessing.py   # Text preprocessing
│   ├── chunking.py        # Document chunking
│   ├── retrieval.py       # FAISS retrieval
│   ├── llm_generator.py   # Gemini LLM integration
│   └── category_retrieval.py  # Advanced retrieval with reranking
├── index/                 # Generated FAISS index + results
│   ├── faiss.index        # FAISS vector index
│   ├── embeddings.npy     # Document embeddings
│   ├── corpus_chunks.json # Chunked documents
│   ├── corpus_meta.json   # Document metadata
│   └── *.json             # Experiment results
├── requirements.txt       # Python dependencies
├── verify_data.py         # Data quality verification
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Data Quality

```bash
python verify_data.py
```

### 3. Explore in Notebooks

```bash
jupyter notebook
```

Open `notebooks/01_data_exploration.ipynb` to start.

## 📊 Data Statistics

- **Total Documents:** 50
- **Categories:** 8
- **Languages:** Arabic
- **Format:** Plain text with markdown structure
- **Quality:** ✅ All files verified

## 🔧 Components

### Core Pipeline

1. **Preprocessing** (`src/preprocessing.py`)
   - Arabic text normalization
   - Diacritics removal
   - Alef variant normalization
   - Document loading and cleaning

2. **Chunking** (`src/chunking.py`)
   - Paragraph-based chunking
   - Sentence-based chunking
   - Section-based chunking
   - Configurable chunk size and overlap

3. **Retrieval** (`src/retrieval.py`)
   - FAISS-based semantic search
   - Multilingual embeddings (paraphrase-multilingual-mpnet-base-v2)
   - Category filtering
   - Index persistence

4. **Advanced Retrieval** (`src/category_retrieval.py`) ⭐ NEW
   - Per-category FAISS indexes
   - Automatic category detection
   - Two-stage retrieval (embedding + reranking)
   - Cross-encoder reranking (ms-marco-MiniLM-L-6-v2)

5. **LLM Generation** (`src/llm_generator.py`)
   - Google Gemini 2.0 Flash integration
   - Context-aware answer generation
   - Source citation
   - Honest "I don't know" responses

## �  Usage

### Basic Retrieval
```bash
python test_end_to_end.py
```

### Advanced Retrieval with Reranking
```bash
python test_reranked_end_to_end.py
```

### Compare Retrieval Approaches
```bash
python test_category_reranking.py
```

### Run Experiments
```bash
# Test 10 diverse queries
python test_10_queries.py

# Chunking experiments
python chunking_experiments.py
```

## 📊 Development Journey

### Day 1-2: Foundation
- Data collection and preprocessing
- Embedding generation
- FAISS index creation

### Day 3: LLM Integration
- Gemini API integration
- Prompt engineering
- Answer generation

### Day 4: Scientific Validation
- 10 diverse query testing (90% accuracy)
- Chunking experiments (4 configurations)
- Performance metrics (P@K, MRR)

### Day 5: Advanced Techniques ⭐
- Per-category FAISS indexes
- Cross-encoder reranking
- Two-stage retrieval
- Comprehensive comparison

**Total Development Time:** 27.5 hours

## 🎓 Key Features

### What Makes This Professional
1. ✅ **Scientific Validation** - Proper experiments with metrics
2. ✅ **Advanced Techniques** - Two-stage retrieval with reranking
3. ✅ **Honest Evaluation** - 0% hallucination rate
4. ✅ **Production Ready** - Modular, tested, documented
5. ✅ **Comprehensive Testing** - 9 test scripts covering all aspects

### Technical Highlights
- Multilingual embeddings for Arabic text
- FAISS for efficient similarity search
- Cross-encoder reranking for accuracy
- Category-aware retrieval
- LLM-powered answer generation
- Extensive experimentation and validation

## 📚 Documentation

- `PROJECT_SETUP.md` - Initial setup guide
- `DAY1_CHECKPOINT.md` - Data and preprocessing
- `DAY2_CHECKPOINT.md` - Embeddings and FAISS
- `DAY3_CHECKPOINT.md` - LLM integration
- `DAY4_CHECKPOINT.md` - Experiments and validation
- `DAY5_CHECKPOINT.md` - Advanced retrieval techniques
- `COMPLETE_PROJECT_SUMMARY.md` - Full project overview

## 🔬 Research & Learning

This project demonstrates:
- End-to-end RAG system development
- Arabic NLP challenges and solutions
- Trade-offs between speed and accuracy
- When to use advanced techniques vs simple solutions
- Scientific approach to ML system evaluation

## 📄 License

Educational and research purposes.
