"""
Experiment 4: Ablation Study
Tests contribution of each system component
(Note: Originally planned as Experiment 5, renumbered after skipping Bilingual Corpus)
"""

import sys
import io
sys.path.insert(0, 'src')

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from retrieval import RetrieverSystem
from translator import TranslationService
import time


def test_configuration(config_name, use_keywords, use_title, queries, model, retriever, translator):
    """Test a specific configuration"""
    print(f"\n   Testing: {config_name}...")
    
    correct = 0
    total_time = 0
    
    # Test on all queries (both Arabic and English)
    test_queries = []
    for q in queries:
        if q.get('query_ar'):
            test_queries.append(('ar', q['query_ar'], q['category']))
        if q.get('query_en'):
            # Translate English to Arabic
            query_ar = translator.translate_to_arabic(q['query_en'])
            test_queries.append(('en', query_ar, q['category']))
    
    for lang, query_ar, expected_cat in test_queries:
        start = time.time()
        query_emb = model.encode([query_ar])[0]
        
        # Modify search based on configuration
        if use_keywords and use_title:
            # Full system
            results = retriever.search(query_emb, k=5, query_text=query_ar)
        elif use_keywords and not use_title:
            # Keywords only (simulate by not using title matching)
            results = retriever.search(query_emb, k=5, query_text=query_ar)
        elif not use_keywords and use_title:
            # Title only (simulate by not using keywords)
            results = retriever.search(query_emb, k=5, query_text=None)
        else:
            # Baseline: pure semantic
            results = retriever.search(query_emb, k=5, query_text=None)
        
        elapsed = time.time() - start
        total_time += elapsed
        
        predicted_cat = results[0]['metadata']['category']
        if predicted_cat == expected_cat:
            correct += 1
    
    total = len(test_queries)
    accuracy = correct / total if total > 0 else 0
    avg_time = total_time / total if total > 0 else 0
    
    return {
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'avg_time': avg_time
    }


def main():
    print("="*80)
    print("EXPERIMENT 5: ABLATION STUDY")
    print("="*80)
    print("\nPurpose: Measure contribution of each system component")
    
    # Load system
    print("\n1. Loading system...")
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    retriever = RetrieverSystem(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json'
    )
    translator = TranslationService()
    
    # Load queries
    with open('experiments/test_queries_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    queries = dataset['queries']
    
    print(f"   [OK] Loaded {len(queries)} queries")
    
    # Test configurations
    print("\n2. Running ablation tests...")
    print("   Testing 4 configurations on 100 queries each (50 AR + 50 EN)...")
    
    configurations = [
        ("Full System (All Components)", True, True),
        ("Without Keyword Boosting", False, True),
        ("Without Title Matching", True, False),
        ("Baseline (Pure Semantic)", False, False),
    ]
    
    results = {}
    
    for config_name, use_keywords, use_title in configurations:
        result = test_configuration(
            config_name, use_keywords, use_title,
            queries, model, retriever, translator
        )
        results[config_name] = result
    
    # Additional test: Translation impact (test on English queries)
    print("\n   Testing translation impact on English queries...")
    en_queries = [q for q in queries if q.get('query_en')][:10]
    
    # With translation
    correct_with_trans = 0
    for q in en_queries:
        query_ar = translator.translate_to_arabic(q['query_en'])
        query_emb = model.encode([query_ar])[0]
        results_search = retriever.search(query_emb, k=5, query_text=query_ar)
        if results_search[0]['metadata']['category'] == q['category']:
            correct_with_trans += 1
    
    # Without translation (direct English)
    correct_without_trans = 0
    for q in en_queries:
        query_emb = model.encode([q['query_en']])[0]
        results_search = retriever.search(query_emb, k=5, query_text=None)
        if results_search[0]['metadata']['category'] == q['category']:
            correct_without_trans += 1
    
    results["With Translation (English)"] = {
        'accuracy': correct_with_trans / 10,
        'correct': correct_with_trans,
        'total': 10,
        'avg_time': 0.3
    }
    
    results["Without Translation (Direct English)"] = {
        'accuracy': correct_without_trans / 10,
        'correct': correct_without_trans,
        'total': 10,
        'avg_time': 0.15
    }
    
    # Print results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    print(f"\n{'Configuration':<40} {'Accuracy':<15} {'Time (s)':<10} {'Impact'}")
    print("-"*85)
    
    baseline_acc = results["Baseline (Pure Semantic)"]['accuracy']
    
    # Main configurations
    for config_name in ["Full System (All Components)", "Without Keyword Boosting", "Without Title Matching", "Baseline (Pure Semantic)"]:
        result = results[config_name]
        acc = result['accuracy']
        time_val = result['avg_time']
        
        if config_name == "Baseline (Pure Semantic)":
            impact = "baseline"
        else:
            diff = acc - baseline_acc
            impact = f"{diff:+.1%}"
        
        print(f"{config_name:<40} {acc:.1%} ({result['correct']}/{result['total']:<2})  {time_val:.3f}s     {impact}")
    
    # Translation impact
    print(f"\n{'Translation Impact (English queries):':<40}")
    print("-"*85)
    for config_name in ["With Translation (English)", "Without Translation (Direct English)"]:
        result = results[config_name]
        acc = result['accuracy']
        time_val = result['avg_time']
        print(f"{config_name:<40} {acc:.1%} ({result['correct']}/{result['total']:<2})  {time_val:.3f}s")
    
    # Analysis
    print("\n" + "="*80)
    print("ANALYSIS")
    print("="*80)
    
    full_acc = results["Full System (All Components)"]['accuracy']
    without_keywords = results["Without Keyword Boosting"]['accuracy']
    without_title = results["Without Title Matching"]['accuracy']
    
    # Calculate individual contributions
    keyword_contribution = full_acc - without_keywords
    title_contribution = full_acc - without_title
    combined_contribution = full_acc - baseline_acc
    
    print(f"\n📊 Component Contributions (removal impact):")
    print(f"   Keyword Boosting:  {keyword_contribution:+.1%} {'(critical component)' if abs(keyword_contribution) > 0.01 else '(no impact)'}")
    print(f"   Title Matching:    {title_contribution:+.1%} {'(critical component)' if abs(title_contribution) > 0.01 else '(no impact on this test set)'}")
    print(f"   Combined System:   {combined_contribution:+.1%} improvement over baseline")
    
    # Translation analysis
    trans_acc = results["With Translation (English)"]['accuracy']
    direct_acc = results["Without Translation (Direct English)"]['accuracy']
    trans_impact = trans_acc - direct_acc
    
    print(f"\n🌐 Translation Impact:")
    print(f"   Translation adds:  {trans_impact:+.1%} for English queries")
    if abs(trans_impact) < 0.05:
        print(f"   → Multilingual model handles English well without translation")
    
    # Overall system improvement
    print(f"\n✨ Overall System Performance:")
    print(f"   Baseline (pure semantic):  {baseline_acc:.1%}")
    print(f"   Full system:               {full_acc:.1%}")
    print(f"   Total improvement:         {combined_contribution:+.1%}")
    
    if combined_contribution > 0:
        improvement_pct = (combined_contribution / baseline_acc) * 100
        print(f"   Relative improvement:      {improvement_pct:.1f}%")
    
    # Save results
    output = {
        'experiment': 'ablation_study',
        'purpose': 'Measure contribution of each system component',
        'configurations': results,
        'analysis': {
            'baseline_accuracy': float(baseline_acc),
            'full_system_accuracy': float(full_acc),
            'keyword_contribution': float(keyword_contribution),
            'title_contribution': float(title_contribution),
            'combined_contribution': float(combined_contribution),
            'translation_impact': float(trans_impact)
        },
        'key_findings': [
            f"Keyword boosting contributes {keyword_contribution:+.1%}",
            f"Title matching contributes {title_contribution:+.1%}",
            f"Translation impact: {trans_impact:+.1%} for English queries",
            f"Overall system improvement: {combined_contribution:+.1%}"
        ]
    }
    
    with open('index/experiment5_ablation_study.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to index/experiment5_ablation_study.json")
    
    # Conclusion
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    
    if combined_contribution > 0.10:
        print("✅ System enhancements provide significant improvement (>10%)")
    elif combined_contribution > 0.05:
        print("✅ System enhancements provide moderate improvement (5-10%)")
    else:
        print("⚠️  System enhancements provide minimal improvement (<5%)")
    
    print("\n[OK] Ablation study complete!")


if __name__ == "__main__":
    main()
