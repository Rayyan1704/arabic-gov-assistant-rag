# Day 4: Evaluation & Experiments

## Overview

This is the **most critical day** - it separates you from tutorial-followers. You're doing real ML engineering: hypothesis testing, metric evaluation, and scientific experimentation.

## What You're Testing

### Hypothesis
"Different chunk sizes affect retrieval quality"

### Variables
- **Independent**: Chunk size (256, 512, 768, 1024)
- **Dependent**: Retrieval accuracy (P@1, P@3, P@5, MRR)
- **Control**: Same documents, same model, same test queries

## Evaluation Metrics

### Precision@1 (P@1)
**Question**: Is the top result from the correct category?
- **1.0** = Perfect (top result always correct)
- **0.5** = 50% of queries get correct top result
- **0.0** = Never gets it right

### Precision@3 (P@3)
**Question**: How many of the top 3 results are relevant?
- **1.0** = All top 3 are relevant
- **0.67** = 2 out of 3 are relevant
- **0.33** = 1 out of 3 is relevant

### Precision@5 (P@5)
**Question**: How many of the top 5 results are relevant?
- Similar to P@3 but for top 5

### Mean Reciprocal Rank (MRR)
**Question**: On average, what position is the first relevant result?
- **1.0** = Always rank 1
- **0.5** = Average rank 2
- **0.33** = Average rank 3

**Formula**: MRR = 1 / (position of first relevant result)

## Test Set (20 Queries)

### Transportation (5 queries)
```
كيف أحصل على رخصة ليموزين؟
ما هي خطوات تأجير السيارات؟
كيف أحصل على ترخيص نقل الأسماك؟
ما هي إجراءات الحصول على رخصة شحن جوي؟
كيف أطلب تعميم على مركبة؟
```

### Education (5 queries)
```
كيف أسجل في مقررات جامعة قطر؟
ما هي خطوات طلب كشف الدرجات؟
كيف أتقدم للقبول في جامعة حمد بن خليفة؟
كيف أنسحب من جامعة قطر؟
أين أجد دليل المراكز البحثية في قطر؟
```

### Health (5 queries)
```
كيف أطلب استشارة طبية؟
كيف أحصل على تقرير طبي من حمد؟
كيف أتواصل مع مؤسسة حمد للاستشارات العاجلة؟
كيف أتقدم للتوظيف في مؤسسة حمد الطبية؟
كيف أحصل على ترخيص ممارس صحي؟
```

### Business (5 queries)
```
كيف أقدم عروض المناقصات؟
كيف أحصل على شهادة تأكيد استلام الطلب؟
كيف أسجل نفسي كمكلف في الضرائب؟
كيف أعيد تفعيل رخصة تجارية؟
كيف أحصل على تمويل من بنك قطر للتنمية؟
```

## Experiment Configurations

| Config | Chunk Size | Overlap | Expected Chunks |
|--------|-----------|---------|-----------------|
| 1 | 256 | 64 | ~68 |
| 2 | 512 | 128 | ~34 (current) |
| 3 | 768 | 192 | ~23 |
| 4 | 1024 | 256 | ~17 |

## Expected Results

### Hypothesis Predictions

**Small chunks (256)**
- ✅ More granular matching
- ❌ May lose context
- ❌ More chunks = slower

**Medium chunks (512)** - Current
- ✅ Good balance
- ✅ Preserves context
- ✅ Fast retrieval

**Large chunks (768-1024)**
- ✅ Maximum context
- ❌ Less precise matching
- ✅ Fewer chunks

## How to Run

```bash
jupyter notebook notebooks/07_evaluation_experiments.ipynb
```

**Time**: ~15-20 minutes (depending on your machine)

## What You'll Learn

### 1. Evaluation Methodology
- How to create test sets
- How to measure retrieval quality
- How to compare configurations

### 2. Trade-offs
- Chunk size vs. accuracy
- Context vs. precision
- Speed vs. quality

### 3. Scientific Thinking
- Hypothesis → Experiment → Analysis
- Metric selection
- Error analysis

## Interpreting Results

### Good Results
- **P@1 > 0.8**: Excellent top-1 accuracy
- **P@3 > 0.7**: Good top-3 coverage
- **MRR > 0.8**: Relevant results appear early

### Acceptable Results
- **P@1 > 0.6**: Decent accuracy
- **P@3 > 0.5**: Reasonable coverage
- **MRR > 0.6**: Relevant results in top 2-3

### Poor Results
- **P@1 < 0.5**: Needs improvement
- **P@3 < 0.4**: Poor coverage
- **MRR < 0.5**: Relevant results too low

## Error Analysis

When a query fails (P@1 = 0), ask:

### 1. Is the query ambiguous?
```
"كيف أحصل على رخصة؟"  # Which license?
```

### 2. Is the expected category wrong?
```
Query about "شهادة من وزارة المواصلات"
Could be: transportation OR business
```

### 3. Is preprocessing too aggressive?
```
Original: "ليموزين"
After normalization: Lost distinctive features?
```

### 4. Is the document missing keywords?
```
Query: "تأجير السيارات"
Document: Only mentions "ليموزين" not "تأجير"
```

## What Makes This Critical

### ❌ Tutorial Approach
- "Here's the code, run it"
- No testing
- No metrics
- No analysis

### ✅ Your Approach
- Created test set (20 queries)
- Tested 4 configurations
- Measured 4 metrics
- Analyzed failures
- **Shows you understand ML engineering**

## Deliverables

After running the notebook, you'll have:

1. **experiment_results.json** - All experiment data
2. **Results table** - Comparing configurations
3. **Best configuration** - Data-driven choice
4. **Error analysis** - Understanding failures
5. **Insights** - What works and why

## Next Steps

### If Results Are Good (P@1 > 0.8)
- ✅ Keep current configuration
- ✅ Document findings
- ✅ Move to deployment

### If Results Are Poor (P@1 < 0.6)
- 🔧 Adjust preprocessing
- 🔧 Try different embedding model
- 🔧 Add query expansion
- 🔧 Implement reranking

## Interview Questions You Can Answer

### "How did you evaluate your RAG system?"
"I created a test set of 20 queries with expected categories, then measured Precision@1, Precision@3, and MRR across different chunk sizes."

### "What chunk size did you choose and why?"
"I tested 4 configurations (256, 512, 768, 1024) and found that 512 with 128 overlap gave the best P@1 score of X.XX while maintaining good context."

### "How do you know your system works?"
"I have quantitative metrics: P@1 of X.XX means the top result is correct XX% of the time. I also did error analysis on failed queries."

### "What would you improve?"
"Based on error analysis, I found that [specific issue]. I would address this by [specific solution]."

## This Is What Separates You

- ✅ You tested hypotheses scientifically
- ✅ You measured with proper metrics
- ✅ You analyzed failures
- ✅ You made data-driven decisions
- ✅ You can explain your choices

**This is real ML engineering, not just following tutorials.**

## Resources

### Learn More About Metrics
- [Information Retrieval Metrics](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval))
- [Understanding MRR](https://en.wikipedia.org/wiki/Mean_reciprocal_rank)
- [Precision and Recall](https://en.wikipedia.org/wiki/Precision_and_recall)

### Similar Work
- [BEIR Benchmark](https://github.com/beir-cellar/beir)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [RAG Evaluation](https://www.pinecone.io/learn/rag-evaluation/)

---

**Ready to run the experiments?**

```bash
jupyter notebook notebooks/07_evaluation_experiments.ipynb
```

**Time to show you're not just following tutorials!** 🚀
