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
    print("="*80)
    print("RESEARCH EXPERIMENTS - DAY 8")
    print("="*80)
    print("\nThis will run:")
    print("1. Experiment 1: Translation Strategies (4 methods)")
    print("2. Experiment 2: Hybrid Retrieval (5 configurations)")
    print("\nEstimated time: 10-15 minutes")
    
    input("\nPress Enter to start...")
    
    experiments = [
        {
            'script': 'experiments/translation_strategies.py',
            'description': 'Experiment 1 - Translation Strategies'
        },
        {
            'script': 'experiments/hybrid_retrieval.py',
            'description': 'Experiment 2 - Hybrid Retrieval'
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
    else:
        print("\n⚠️  Some experiments failed. Check the output above for details.")


if __name__ == "__main__":
    main()
