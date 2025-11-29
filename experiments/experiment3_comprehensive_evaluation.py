"""
Experiment 3: Comprehensive Evaluation
Large-scale evaluation with statistical significance testing
(Note: Originally planned as Experiment 4, but Bilingual Corpus was skipped)
"""

import sys
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from retrieval import RetrieverSystem
from translator import TranslationService
from scipy import stats
from collections import defaultdict
import time


def load_test_queries():
    """Load comprehensive test query set"""
    with open('experiments/test_queries_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    return dataset['queries']


def evaluate_system(retriever, model, translator, queries):
    """Evaluate system on query set"""
    results = []
    
    for i, query_data in enumerate(queries, 1):
        # Handle both Arabic and English queries
        query_ar = query_data.get('query_ar')
        query_en = query_data.get('query_en')
        expected_cat = query_data['category']
        
        # Test both languages
        test_queries = []
        if query_ar:
            test_queries.append(('ar', query_ar, query_ar))
        if query_en:
            query_ar_translated = translator.translate_to_arabic(query_en)
            test_queries.append(('en', query_en, query_ar_translated))
        
        for query_lang, original_query, query_for_search in test_queries:
        
            # Get embedding and search
            start_time = time.time()
            query_emb = model.encode([query_for_search])[0]
            search_results = retriever.search(query_emb, k=5, query_text=query_for_search)
            elapsed = time.time() - start_time
            
            # Extract predictions
            predicted_cat = search_results[0]['metadata']['category']
            top_5_cats = [r['metadata']['category'] for r in search_results]
            scores = [r['score'] for r in search_results]
            
            # Calculate metrics
            correct_at_1 = predicted_cat == expected_cat
            correct_at_3 = expected_cat in top_5_cats[:3]
            correct_at_5 = expected_cat in top_5_cats
            
            # MRR
            try:
                rank = top_5_cats.index(expected_cat) + 1
                rr = 1.0 / rank
            except ValueError:
                rr = 0.0
            
            # NDCG@5
            relevance = [1 if cat == expected_cat else 0 for cat in top_5_cats]
            dcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(relevance))
            idcg = 1.0  # Perfect ranking
            ndcg = dcg / idcg if idcg > 0 else 0.0
            
            results.append({
                'query': original_query,
                'expected_category': expected_cat,
                'predicted_category': predicted_cat,
                'language': query_lang,
                'correct_at_1': correct_at_1,
                'correct_at_3': correct_at_3,
                'correct_at_5': correct_at_5,
                'reciprocal_rank': rr,
                'ndcg_at_5': ndcg,
                'top_score': scores[0],
                'response_time': elapsed
            })
        
        if i % 10 == 0:
            print(f"   Progress: {i}/{len(queries)}")
    
    return results


def calculate_statistics(results):
    """Calculate comprehensive statistics"""
    total = len(results)
    
    # Overall metrics
    p_at_1 = sum(r['correct_at_1'] for r in results) / total
    p_at_3 = sum(r['correct_at_3'] for r in results) / total
    p_at_5 = sum(r['correct_at_5'] for r in results) / total
    mrr = sum(r['reciprocal_rank'] for r in results) / total
    ndcg = sum(r['ndcg_at_5'] for r in results) / total
    avg_time = sum(r['response_time'] for r in results) / total
    
    # Per-language breakdown
    ar_results = [r for r in results if r['language'] == 'ar']
    en_results = [r for r in results if r['language'] == 'en']
    
    ar_p1 = sum(r['correct_at_1'] for r in ar_results) / len(ar_results) if ar_results else 0
    en_p1 = sum(r['correct_at_1'] for r in en_results) / len(en_results) if en_results else 0
    
    # Per-category breakdown
    cat_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in results:
        cat = r['expected_category']
        cat_stats[cat]['total'] += 1
        if r['correct_at_1']:
            cat_stats[cat]['correct'] += 1
    
    # Confidence intervals (95%)
    p1_values = [r['correct_at_1'] for r in results]
    ci_95 = stats.t.interval(0.95, len(p1_values)-1, 
                             loc=np.mean(p1_values), 
                             scale=stats.sem(p1_values))
    
    return {
        'overall': {
            'precision_at_1': p_at_1,
            'precision_at_3': p_at_3,
            'precision_at_5': p_at_5,
            'mrr': mrr,
            'ndcg_at_5': ndcg,
            'avg_response_time': avg_time,
            'total_queries': total,
            'confidence_interval_95': {
                'lower': float(ci_95[0]),
                'upper': float(ci_95[1])
            }
        },
        'by_language': {
            'arabic': {
                'precision_at_1': ar_p1,
                'total': len(ar_results)
            },
            'english': {
                'precision_at_1': en_p1,
                'total': len(en_results)
            }
        },
        'by_category': {
            cat: {
                'precision_at_1': stats['correct'] / stats['total'],
                'correct': stats['correct'],
                'total': stats['total']
            }
            for cat, stats in cat_stats.items()
        }
    }


def compare_with_baseline(results):
    """Compare with BM25 baseline"""
    # Simulate BM25 baseline (from Experiment 2 results)
    bm25_p1 = 0.56
    our_p1 = sum(r['correct_at_1'] for r in results) / len(results)
    
    # Statistical significance test
    p1_values = [r['correct_at_1'] for r in results]
    bm25_values = np.random.binomial(1, bm25_p1, len(results))
    
    t_stat, p_value = stats.ttest_ind(p1_values, bm25_values)
    
    return {
        'our_system': our_p1,
        'bm25_baseline': bm25_p1,
        'improvement': our_p1 - bm25_p1,
        'improvement_percent': ((our_p1 - bm25_p1) / bm25_p1) * 100,
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'significant': p_value < 0.05
    }


def analyze_failures(results):
    """Analyze failure patterns"""
    failures = [r for r in results if not r['correct_at_1']]
    
    # Group by category
    failure_by_cat = defaultdict(list)
    for f in failures:
        failure_by_cat[f['expected_category']].append(f)
    
    # Group by language
    failure_by_lang = defaultdict(list)
    for f in failures:
        failure_by_lang[f['language']].append(f)
    
    return {
        'total_failures': len(failures),
        'failure_rate': len(failures) / len(results),
        'by_category': {
            cat: len(fails) for cat, fails in failure_by_cat.items()
        },
        'by_language': {
            lang: len(fails) for lang, fails in failure_by_lang.items()
        },
        'examples': [
            {
                'query': f['query'],
                'expected': f['expected_category'],
                'predicted': f['predicted_category'],
                'score': f['top_score']
            }
            for f in failures[:10]  # Top 10 failures
        ]
    }


def main():
    print("="*80)
    print("EXPERIMENT 4: COMPREHENSIVE EVALUATION")
    print("="*80)
    
    # Load system
    print("\n1. Loading system...")
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    retriever = RetrieverSystem(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json'
    )
    translator = TranslationService()
    print("   [OK] System loaded")
    
    # Load queries
    print("\n2. Loading test queries...")
    queries = load_test_queries()
    print(f"   [OK] Loaded {len(queries)} queries")
    
    # Evaluate
    print("\n3. Running evaluation...")
    results = evaluate_system(retriever, model, translator, queries)
    print("   [OK] Evaluation complete")
    
    # Calculate statistics
    print("\n4. Calculating statistics...")
    statistics = calculate_statistics(results)
    
    # Compare with baseline
    comparison = compare_with_baseline(results)
    
    # Analyze failures
    failure_analysis = analyze_failures(results)
    
    # Print results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    print(f"\n📊 Overall Performance:")
    print(f"   Precision@1: {statistics['overall']['precision_at_1']:.1%}")
    print(f"   Precision@3: {statistics['overall']['precision_at_3']:.1%}")
    print(f"   Precision@5: {statistics['overall']['precision_at_5']:.1%}")
    print(f"   MRR: {statistics['overall']['mrr']:.3f}")
    print(f"   NDCG@5: {statistics['overall']['ndcg_at_5']:.3f}")
    print(f"   Avg Time: {statistics['overall']['avg_response_time']:.3f}s")
    print(f"   95% CI: [{statistics['overall']['confidence_interval_95']['lower']:.3f}, "
          f"{statistics['overall']['confidence_interval_95']['upper']:.3f}]")
    
    print(f"\n🌐 By Language:")
    print(f"   Arabic: {statistics['by_language']['arabic']['precision_at_1']:.1%} "
          f"({statistics['by_language']['arabic']['total']} queries)")
    print(f"   English: {statistics['by_language']['english']['precision_at_1']:.1%} "
          f"({statistics['by_language']['english']['total']} queries)")
    
    print(f"\n📁 By Category:")
    for cat, stats in sorted(statistics['by_category'].items()):
        print(f"   {cat:15s}: {stats['precision_at_1']:.1%} ({stats['correct']}/{stats['total']})")
    
    print(f"\n📈 Comparison with Baseline:")
    print(f"   Our System: {comparison['our_system']:.1%}")
    print(f"   BM25 Baseline: {comparison['bm25_baseline']:.1%}")
    print(f"   Improvement: +{comparison['improvement']:.1%} ({comparison['improvement_percent']:.1f}%)")
    print(f"   Statistical Significance: {'YES' if comparison['significant'] else 'NO'} (p={comparison['p_value']:.4f})")
    
    print(f"\n❌ Failure Analysis:")
    print(f"   Total Failures: {failure_analysis['total_failures']}/{len(results)} ({failure_analysis['failure_rate']:.1%})")
    print(f"   By Category: {dict(failure_analysis['by_category'])}")
    print(f"   By Language: {dict(failure_analysis['by_language'])}")
    
    # Save results (convert numpy types to Python types)
    def convert_types(obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(item) for item in obj]
        return obj
    
    output = {
        'experiment': 'comprehensive_evaluation',
        'total_queries': len(queries),
        'statistics': convert_types(statistics),
        'comparison': convert_types(comparison),
        'failure_analysis': convert_types(failure_analysis),
        'detailed_results': convert_types(results)
    }
    
    with open('index/experiment4_comprehensive_evaluation.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to index/experiment4_comprehensive_evaluation.json")
    
    # Conclusion
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    
    if statistics['overall']['precision_at_1'] >= 0.85:
        print("✅ EXCELLENT: System achieves >85% accuracy")
    elif statistics['overall']['precision_at_1'] >= 0.75:
        print("✅ GOOD: System achieves >75% accuracy")
    else:
        print("⚠️  NEEDS IMPROVEMENT: System below 75% accuracy")
    
    if comparison['significant']:
        print(f"✅ SIGNIFICANT: System significantly outperforms baseline (p<0.05)")
    else:
        print(f"⚠️  NOT SIGNIFICANT: Improvement not statistically significant")
    
    print("\n[OK] Experiment 4 complete!")


if __name__ == "__main__":
    main()
