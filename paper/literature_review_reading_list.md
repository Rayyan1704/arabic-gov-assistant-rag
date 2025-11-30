# Literature Review Reading List

**Goal:** Read abstracts + skim results sections of these papers  
**Time:** 1-2 days  
**Total Papers:** 20 (organized by topic)

---

## 1. RAG Systems (Core - MUST READ) - 5 papers

### 📄 1.1 Original RAG Paper
**Title:** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"  
**Authors:** Lewis et al. (2020)  
**Venue:** NeurIPS 2020  
**Link:** https://arxiv.org/abs/2005.11401  
**Why:** The foundational RAG paper - defines the paradigm  
**What to note:** Architecture, training approach, evaluation metrics

### 📄 1.2 Recent RAG Survey
**Title:** "Retrieval-Augmented Generation for Large Language Models: A Survey"  
**Authors:** Gao et al. (2023)  
**Venue:** arXiv 2023  
**Link:** https://arxiv.org/abs/2312.10997  
**Why:** Comprehensive overview of RAG techniques  
**What to note:** Different RAG architectures, evaluation approaches

### 📄 1.3 Dense Retrieval
**Title:** "Dense Passage Retrieval for Open-Domain Question Answering"  
**Authors:** Karpukhin et al. (2020)  
**Venue:** EMNLP 2020  
**Link:** https://arxiv.org/abs/2004.04906  
**Why:** Dense retrieval (what you use) vs sparse (BM25)  
**What to note:** Why dense retrieval works, training approach

### 📄 1.4 Contriever
**Title:** "Unsupervised Dense Information Retrieval with Contrastive Learning"  
**Authors:** Izacard et al. (2022)  
**Venue:** TMLR 2022  
**Link:** https://arxiv.org/abs/2112.09118  
**Why:** Modern dense retrieval approach  
**What to note:** Contrastive learning for retrieval

### 📄 1.5 REALM
**Title:** "REALM: Retrieval-Augmented Language Model Pre-Training"  
**Authors:** Guu et al. (2020)  
**Venue:** ICML 2020  
**Link:** https://arxiv.org/abs/2002.08909  
**Why:** Alternative RAG approach  
**What to note:** End-to-end training of retriever + LM

---

## 2. Arabic NLP (Domain-Specific) - 4 papers

### 📄 2.1 AraBERT
**Title:** "AraBERT: Transformer-based Model for Arabic Language Understanding"  
**Authors:** Antoun et al. (2020)  
**Venue:** OSACT 2020  
**Link:** https://arxiv.org/abs/2003.00104  
**Why:** Key Arabic language model  
**What to note:** Arabic text challenges, preprocessing

### 📄 2.2 Arabic NLP Survey
**Title:** "A Survey on Arabic Natural Language Processing"  
**Authors:** Guellil et al. (2021)  
**Venue:** Artificial Intelligence Review  
**Link:** https://link.springer.com/article/10.1007/s10462-020-09927-0  
**Why:** Overview of Arabic NLP challenges  
**What to note:** Morphology, dialects, resources

### 📄 2.3 AraGPT
**Title:** "AraGPT2: Pre-Trained Transformer for Arabic Language Generation"  
**Authors:** Antoun et al. (2021)  
**Venue:** WANLP 2021  
**Link:** https://arxiv.org/abs/2012.15520  
**Why:** Arabic text generation  
**What to note:** Arabic-specific challenges

### 📄 2.4 Arabic Question Answering
**Title:** "Arabic Question Answering: A Survey and Analysis"  
**Authors:** Trigui et al. (2010)  
**Venue:** LREC 2010  
**Why:** Arabic QA systems overview  
**What to note:** Challenges specific to Arabic QA

---

## 3. Multilingual & Cross-Lingual Retrieval - 5 papers

### 📄 3.1 Multilingual Sentence Embeddings
**Title:** "Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation"  
**Authors:** Reimers & Gurevych (2020)  
**Venue:** EMNLP 2020  
**Link:** https://arxiv.org/abs/2004.09813  
**Why:** The model you use (paraphrase-multilingual-mpnet)  
**What to note:** How multilingual embeddings work

### 📄 3.2 mBERT
**Title:** "Multilingual BERT: Unsupervised Cross-lingual Representation Learning"  
**Authors:** Devlin et al. (2019)  
**Venue:** NAACL 2019  
**Link:** https://arxiv.org/abs/1810.04805  
**Why:** Foundation of multilingual models  
**What to note:** Cross-lingual transfer

### 📄 3.3 Cross-Lingual Retrieval
**Title:** "Cross-Lingual Retrieval for Iterative Self-Supervised Training"  
**Authors:** Tran et al. (2020)  
**Venue:** NeurIPS 2020  
**Link:** https://arxiv.org/abs/2006.09526  
**Why:** Cross-lingual retrieval techniques  
**What to note:** Translation vs multilingual embeddings

### 📄 3.4 LASER
**Title:** "Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer"  
**Authors:** Artetxe & Schwenk (2019)  
**Venue:** ACL 2019  
**Link:** https://arxiv.org/abs/1812.10464  
**Why:** Alternative multilingual embedding approach  
**What to note:** Zero-shot cross-lingual capabilities

### 📄 3.5 Translation for Retrieval
**Title:** "Neural Machine Translation for Query Construction and Composition"  
**Authors:** Sasaki et al. (2018)  
**Venue:** arXiv 2018  
**Link:** https://arxiv.org/abs/1806.07125  
**Why:** Translation strategies for retrieval  
**What to note:** When translation helps vs hurts

---

## 4. Hybrid Search & Reranking - 4 papers

### 📄 4.1 BM25 + Dense
**Title:** "Complement Lexical Retrieval Model with Semantic Residual Embeddings"  
**Authors:** Gao et al. (2021)  
**Venue:** ECIR 2021  
**Link:** https://arxiv.org/abs/2004.13969  
**Why:** Hybrid sparse + dense retrieval  
**What to note:** When hybrid helps

### 📄 4.2 ColBERT
**Title:** "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction"  
**Authors:** Khattab & Zaharia (2020)  
**Venue:** SIGIR 2020  
**Link:** https://arxiv.org/abs/2004.12832  
**Why:** Alternative dense retrieval approach  
**What to note:** Late interaction mechanism

### 📄 4.3 Cross-Encoder Reranking
**Title:** "Passage Re-ranking with BERT"  
**Authors:** Nogueira & Cho (2019)  
**Venue:** arXiv 2019  
**Link:** https://arxiv.org/abs/1901.04085  
**Why:** Reranking with cross-encoders (what you use)  
**What to note:** Two-stage retrieval benefits

### 📄 4.4 RankGPT
**Title:** "Is ChatGPT Good at Search? Investigating Large Language Models as Re-Ranking Agents"  
**Authors:** Sun et al. (2023)  
**Venue:** EMNLP 2023  
**Link:** https://arxiv.org/abs/2304.09542  
**Why:** LLM-based reranking (recent)  
**What to note:** LLM reranking vs traditional

---

## 5. Evaluation & Benchmarks - 2 papers

### 📄 5.1 BEIR Benchmark
**Title:** "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"  
**Authors:** Thakur et al. (2021)  
**Venue:** NeurIPS 2021  
**Link:** https://arxiv.org/abs/2104.08663  
**Why:** Standard IR evaluation benchmark  
**What to note:** Evaluation metrics, zero-shot evaluation

### 📄 5.2 MTEB
**Title:** "MTEB: Massive Text Embedding Benchmark"  
**Authors:** Muennighoff et al. (2023)  
**Venue:** EACL 2023  
**Link:** https://arxiv.org/abs/2210.07316  
**Why:** Embedding evaluation benchmark  
**What to note:** How to evaluate embeddings

---

## Reading Strategy

### For Each Paper:

1. **Abstract (2 min):**
   - What problem does it solve?
   - What's their approach?
   - What are the main results?

2. **Introduction (5 min):**
   - Why is this problem important?
   - What are the limitations of prior work?

3. **Methodology (skim, 3 min):**
   - High-level approach
   - Key technical details

4. **Results (10 min - IMPORTANT):**
   - What metrics do they use?
   - What baselines do they compare against?
   - What are the main findings?
   - Look at tables and figures

5. **Conclusion (2 min):**
   - Main takeaways
   - Limitations mentioned

**Total per paper:** ~20-25 minutes  
**Total time:** 20 papers × 25 min = ~8 hours (spread over 1-2 days)

---

## How to Cite in Your Paper

### In Related Work section:

**RAG Systems:**
"Retrieval-Augmented Generation (RAG) combines retrieval with generation [Lewis et al., 2020; Guu et al., 2020]. Recent work has explored dense retrieval [Karpukhin et al., 2020] and contrastive learning approaches [Izacard et al., 2022]."

**Arabic NLP:**
"Arabic presents unique challenges including rich morphology and dialectal variation [Guellil et al., 2021]. Recent models like AraBERT [Antoun et al., 2020] and AraGPT [Antoun et al., 2021] have advanced Arabic NLP."

**Multilingual Retrieval:**
"Multilingual sentence embeddings [Reimers & Gurevych, 2020] enable cross-lingual retrieval without translation. Alternative approaches include LASER [Artetxe & Schwenk, 2019] and mBERT [Devlin et al., 2019]."

**Hybrid Search:**
"Hybrid retrieval combines sparse (BM25) and dense methods [Gao et al., 2021]. Two-stage retrieval with reranking [Nogueira & Cho, 2019] improves accuracy at the cost of latency."

---

## Next Steps

1. **Read these 20 papers** (abstracts + results)
2. **Take notes** on key findings relevant to your work
3. **Identify gaps** your work addresses
4. **Write Related Work section** (I'll help with template)

**Start with the "MUST READ" papers (1.1-1.3) first!**
