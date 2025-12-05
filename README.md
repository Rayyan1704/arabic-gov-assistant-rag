# Cross-Lingual RAG for Arabic Government Services

A bilingual (Arabic-English) Retrieval-Augmented Generation system achieving **99% category accuracy** (84% source accuracy) on government service queries. Built with multilingual embeddings and domain-specific keyword boosting.

**Author:** Mohammed Aaqil Rayyan  
**Paper:** [Cross-Lingual Retrieval-Augmented Generation for Arabic Government Services](paper/main.tex)

---

## Key Results

| Metric | Formal Queries | Messy Queries |
|--------|----------------|---------------|
| Category P@1 | 99% | 84% |
| Category P@3 | 99% | 89% |
| Source P@1 | 84% | 51% |
| Source P@3 | 92% | 69% |
| Source P@5 | 94% | 78% |

| Language/Type | Accuracy |
|---------------|----------|
| Arabic | 100% (50/50) |
| English | 98% (49/50) |
| Dialectal Arabic | 90% (27/30) |
| vs BM25 Baseline | +43pp (p < 0.0001) |

*Category = correct service category; Source = exact correct document*

---

## What This Does

Helps people find information about Qatar government services in Arabic or English. Searches through 51 documents across 8 categories and provides accurate answers in under a second.

**Capabilities:**
- Handles queries in Arabic or English
- Generates contextual answers using Google Gemini
- Shows source documents used
- Runs through a web interface (Streamlit)

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/Rayyan1704/arabic-gov-assistant-rag.git
cd arabic-gov-assistant-rag
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Add your API key
echo GEMINI_API_KEY=your_key_here > .env

# Run the app
streamlit run app.py
```

---

## Project Structure

```
arabic-gov-assistant-rag/
├── app.py                      # Streamlit web interface
├── run_all_experiments.py      # Run all experiments
│
├── src/                        # Core modules
│   ├── preprocessing.py        # Arabic text normalisation
│   ├── chunking.py             # Document chunking
│   ├── retrieval.py            # FAISS retrieval + keyword boosting
│   ├── llm_generator.py        # Gemini integration
│   └── translator.py           # Google Translate
│
├── experiments/                # Research experiments (5)
│   ├── experiment1_translation_strategies.py
│   ├── experiment2_hybrid_retrieval.py
│   ├── experiment3_comprehensive_evaluation.py
│   ├── experiment4_robustness_evaluation.py
│   └── experiment5_ablation_study.py
│
├── data/                       # 51 documents, 8 categories
│   ├── business/
│   ├── culture/
│   ├── education/
│   ├── health/
│   ├── housing/
│   ├── info/
│   ├── justice/
│   └── transportation/
│
├── methodology/                # Technical documentation
│   ├── METHODOLOGY.md          # Complete system design
│   ├── EXPERIMENTS.md          # All 5 experiments
│   ├── RESULTS.md              # Findings and analysis
│   └── DEVELOPMENT_LOG.md      # Timeline and challenges
│
├── paper/                      # Research paper (LaTeX)
│   ├── main.tex
│   ├── sections/               # Paper sections
│   ├── figures/                # Generated figures
│   └── references.bib
│
└── index/                      # Generated indexes
    ├── embeddings.npy
    ├── faiss.index
    └── corpus_chunks.json
```

---

## Research Findings

### 1. Multilingual Embeddings Eliminate Translation
- 100% accuracy on English queries without translation
- Saves 0.23s latency per query
- No translation errors

### 2. Pure Semantic Search Outperforms Hybrid
- Semantic: 84% P@1
- Hybrid (BM25 + Semantic): 70-80% P@1
- High-quality embeddings already capture lexical information

### 3. Keyword Boosting is Critical
- Adds +8% accuracy (91% → 99%)
- Domain-specific terms need explicit boosting
- Title matching contributes 0%

### 4. Strong Robustness
- Dialectal Arabic: 90%
- Short phrases: 84%
- Broken grammar: 80%
- Single words: 80%
- Only 15% drop from formal queries
- Source accuracy: 78% at P@5 on messy queries

---

## Technology Stack

- **Embeddings:** paraphrase-multilingual-mpnet-base-v2
- **Vector Index:** FAISS IndexFlatIP
- **LLM:** Google Gemini 2.0 Flash
- **Translation:** Google Translate API
- **UI:** Streamlit
- **Language:** Python 3.12

---

## Running Experiments

```bash
# Run all experiments
python run_all_experiments.py

# Run individual experiments
python experiments/experiment1_translation_strategies.py
python experiments/experiment2_hybrid_retrieval.py
python experiments/experiment3_comprehensive_evaluation.py
python experiments/experiment4_robustness_evaluation.py
python experiments/experiment5_ablation_study.py
```

---

## Documentation

- [methodology/METHODOLOGY.md](methodology/METHODOLOGY.md) - Complete technical approach
- [methodology/EXPERIMENTS.md](methodology/EXPERIMENTS.md) - All 5 experiments detailed
- [methodology/RESULTS.md](methodology/RESULTS.md) - Findings and analysis
- [methodology/DEVELOPMENT_LOG.md](methodology/DEVELOPMENT_LOG.md) - Timeline and challenges

---

## Limitations

- Small corpus (51 documents)
- Single domain (Qatar government services)
- Several small categories (5-8 documents each)
- Single-word queries challenging (80% category accuracy)

---

## Citation

```bibtex
@misc{rayyan2025crosslingual,
  title={Cross-Lingual Retrieval-Augmented Generation for Arabic Government Services},
  author={Mohammed Aaqil Rayyan},
  year={2025},
  url={https://github.com/Rayyan1704/arabic-gov-assistant-rag}
}
```

---

## Licence

MIT Licence. See LICENSE file for details.
