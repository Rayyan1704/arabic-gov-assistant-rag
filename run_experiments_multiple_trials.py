"""
Run all experiments with multiple trials for statistical validity.
This ensures reproducibility and provides mean ± std deviation for results.
"""

import json
import numpy as np
import random
from pathlib import Path
import sys
sys.path.insert(0, 'experiments')

from experiment1_translation_strategies import run_experiment as exp1
from experiment2_hybrid_retrieval import run_experiment as exp2
from experiment3_comprehensive_evaluation import run_experiment as exp3
from experiment4_ablation_study import run_experiment as exp4

# Number of trials
NUM_TRIALS = 3
SEEDS = [42, 123, 456]  # Fixed seeds for reproducibility

def set_seed(seed):
    """Set random seed for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)

def aggregate_results(results_list, experiment_name):
    """Aggregate results from multiple trials"""
    
    # Extract key metrics
    if experiment_name == "experiment1":
        # Translation strategies
        metrics = {}
        for strategy in results_list[0]['results'].keys():
            accuracies = [r['results'][strategy]['precision_at_1'] for r in results_list]
            times = [r['results'][strategy]['avg_time'] for r in results_list]
            
            metrics[strategy] = {
                'precision_at_1_mean': np.mean(accuracies),
                'precision_at_1_std': np.std(accuracies),
                'avg_time_mean': np.mean(times),
                'avg_time_std': np.std(times)
            }
        return metrics
    
    elif experiment_name == "experiment2":
        # Hybrid retrieval
        metrics = {}
        for method in results_list[0]['results'].keys():
            accuracies = [r['results'][method]['precision_at_1'] for r in results_list]
            
            metrics[method] = {
                'precision_at_1_mean': np.mean(accuracies),
                'precision_at_1_std': np.std(accuracies)
            }
        return metrics
    
    elif experiment_name == "experiment3":
        # Comprehensive evaluation
        accuracies = [r['statistics']['overall']['precision_at_1'] for r in results_list]
        mrrs = [r['statistics']['overall']['mrr'] for r in results_list]
        times = [r['statistics']['overall']['avg_response_time'] for r in results_list]
        
        return {
            'precision_at_1_mean': np.mean(accuracies),
            'precision_at_1_std': np.std(accuracies),
            'mrr_mean': np.mean(mrrs),
            'mrr_std': np.std(mrrs),
            'avg_time_mean': np.mean(times),
            'avg_time_std': np.std(times)
        }
    
    elif experiment_name == "experiment4":
        # Ablation study
        metrics = {}
        for config in results_list[0]['configurations'].keys():
            accuracies = [r['configurations'][config]['accuracy'] for r in results_list]
            
            metrics[config] = {
                'accuracy_mean': np.mean(accuracies),
                'accuracy_std': np.std(accuracies)
            }
        return metrics

def main():
    print("="*80)
    print("RUNNING EXPERIMENTS WITH MULTIPLE TRIALS")
    print("="*80)
    print(f"\nNumber of trials: {NUM_TRIALS}")
    print(f"Seeds: {SEEDS}")
    print()
    
    all_results = {
        'experiment1': [],
        'experiment2': [],
        'experiment3': [],
        'experiment4': []
    }
    
    # Run each experiment NUM_TRIALS times
    for trial in range(NUM_TRIALS):
        seed = SEEDS[trial]
        print(f"\n{'='*80}")
        print(f"TRIAL {trial + 1}/{NUM_TRIALS} (seed={seed})")
        print(f"{'='*80}")
        
        set_seed(seed)
        
        # Experiment 1: Translation Strategies
        print(f"\n[Trial {trial+1}] Running Experiment 1: Translation Strategies...")
        try:
            result1 = exp1()
            all_results['experiment1'].append(result1)
            print(f"   ✓ Completed")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Experiment 2: Hybrid Retrieval
        print(f"\n[Trial {trial+1}] Running Experiment 2: Hybrid Retrieval...")
        try:
            result2 = exp2()
            all_results['experiment2'].append(result2)
            print(f"   ✓ Completed")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Experiment 3: Comprehensive Evaluation
        print(f"\n[Trial {trial+1}] Running Experiment 3: Comprehensive Evaluation...")
        try:
            result3 = exp3()
            all_results['experiment3'].append(result3)
            print(f"   ✓ Completed")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        # Experiment 4: Ablation Study
        print(f"\n[Trial {trial+1}] Running Experiment 4: Ablation Study...")
        try:
            result4 = exp4()
            all_results['experiment4'].append(result4)
            print(f"   ✓ Completed")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    # Aggregate results
    print("\n" + "="*80)
    print("AGGREGATING RESULTS")
    print("="*80)
    
    aggregated = {}
    for exp_name, results in all_results.items():
        if results:
            aggregated[exp_name] = aggregate_results(results, exp_name)
            print(f"\n✓ Aggregated {exp_name}")
    
    # Save aggregated results
    output_file = 'index/experiments_multiple_trials.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'num_trials': NUM_TRIALS,
            'seeds': SEEDS,
            'aggregated_results': aggregated,
            'all_trials': all_results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved aggregated results to: {output_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY (Mean ± Std)")
    print("="*80)
    
    if 'experiment3' in aggregated:
        exp3_results = aggregated['experiment3']
        print(f"\nExperiment 3 (Comprehensive Evaluation):")
        print(f"  Precision@1: {exp3_results['precision_at_1_mean']:.3f} ± {exp3_results['precision_at_1_std']:.3f}")
        print(f"  MRR: {exp3_results['mrr_mean']:.3f} ± {exp3_results['mrr_std']:.3f}")
        print(f"  Response Time: {exp3_results['avg_time_mean']:.3f}s ± {exp3_results['avg_time_std']:.3f}s")
    
    if 'experiment4' in aggregated:
        print(f"\nExperiment 4 (Ablation Study):")
        for config, metrics in aggregated['experiment4'].items():
            print(f"  {config}: {metrics['accuracy_mean']:.3f} ± {metrics['accuracy_std']:.3f}")
    
    print("\n" + "="*80)
    print("COMPLETE!")
    print("="*80)
    print(f"\nResults saved to: {output_file}")
    print("You can now use these results in your paper with mean ± std deviation.")

if __name__ == '__main__':
    main()
