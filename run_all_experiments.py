"""
Master script to run all research experiments.
Executes Day 8 experiments in sequence.
"""

import subprocess
import sys
import time


def run_experiment(script_name, description):
    """Run a single experiment script"""
    print("\n" + "="*80)
    print(f"STARTING: {description}")
    print("="*80)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            check=True
        )
        
        elapsed = time.time() - start_time
        print(f"\n✅ {description} completed in {elapsed:.1f}s")
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"\n❌ {description} failed after {elapsed:.1f}s")
        print(f"Error: {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run all research experiments')
    parser.add_argument('--auto', action='store_true', help='Run without prompts (for automation)')
    args = parser.parse_args()
    
    print("="*80)
    print("RESEARCH EXPERIMENTS - ALL 5 EXPERIMENTS")
    print("="*80)
    print("\nThis will run:")
    print("1. Experiment 1: Translation Strategies (4 methods)")
    print("2. Experiment 2: Hybrid Retrieval (5 configurations)")
    print("3. Experiment 3: Formal Queries Evaluation (100 queries)")
    print("4. Experiment 4: Robustness Evaluation (100 messy queries)")
    print("5. Experiment 5: Ablation Study (component analysis)")
    print("\nEstimated time: 5-8 minutes")
    
    if not args.auto:
        input("\nPress Enter to start...")
    
    experiments = [
        {
            'script': 'experiments/experiment1_translation_strategies.py',
            'description': 'Experiment 1 - Translation Strategies'
        },
        {
            'script': 'experiments/experiment2_hybrid_retrieval.py',
            'description': 'Experiment 2 - Hybrid Retrieval'
        },
        {
            'script': 'experiments/experiment3_comprehensive_evaluation.py',
            'description': 'Experiment 3 - Comprehensive Evaluation'
        },
        {
            'script': 'experiments/experiment4_robustness_evaluation.py',
            'description': 'Experiment 4 - Robustness Evaluation'
        },
        {
            'script': 'experiments/experiment5_ablation_study.py',
            'description': 'Experiment 5 - Ablation Study'
        }
    ]
    
    results = []
    total_start = time.time()
    
    for exp in experiments:
        success = run_experiment(exp['script'], exp['description'])
        results.append({
            'experiment': exp['description'],
            'success': success
        })
        
        if not success:
            if args.auto:
                print(f"\n⚠️  {exp['description']} failed. Continuing (--auto mode)...")
            else:
                print(f"\n⚠️  {exp['description']} failed. Continue anyway? (y/n)")
                response = input().strip().lower()
                if response != 'y':
                    print("\nExperiments stopped.")
                    break
    
    # Summary
    total_elapsed = time.time() - total_start
    
    print("\n" + "="*80)
    print("EXPERIMENTS SUMMARY")
    print("="*80)
    
    for result in results:
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"{status} - {result['experiment']}")
    
    successful = sum(1 for r in results if r['success'])
    print(f"\nTotal: {successful}/{len(results)} experiments successful")
    print(f"Total time: {total_elapsed/60:.1f} minutes")
    
    if successful == len(results):
        print("\n🎉 All experiments completed successfully!")
        print("\nResults saved to:")
        print("  - index/experiment1_translation_strategies.json")
        print("  - index/experiment2_hybrid_retrieval.json")
        print("  - index/experiment3_comprehensive_evaluation.json")
        print("  - index/experiment4_robustness_evaluation.json")
        print("  - index/experiment5_ablation_study.json")
    else:
        print("\n⚠️  Some experiments failed. Check the output above for details.")


if __name__ == "__main__":
    main()
