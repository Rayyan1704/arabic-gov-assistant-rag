"""
Generate publication-quality figures for the research paper.
Creates 4 essential figures covering all research questions.
"""

import matplotlib.pyplot as plt
import numpy as np
import json

# Set publication-quality style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 14

# Professional color palette
COLORS = {
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Purple
    'success': '#06A77D',      # Green
    'warning': '#F18F01',      # Orange
    'danger': '#C73E1D',       # Red
    'neutral': '#6C757D',      # Gray
    'light': '#E9ECEF'
}

def save_figure(filename):
    """Save figure in both PNG and PDF formats"""
    plt.savefig(f'paper/figures/{filename}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'paper/figures/{filename}.pdf', bbox_inches='tight')
    print(f"✅ Saved {filename}")
    plt.close()


def fig1_translation_strategies():
    """Figure 1: Translation Strategy Comparison (RQ1)"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Left: Accuracy comparison
    methods = ['Direct\nEnglish', 'Multilingual', 'Translate\n+ Embed', 'Back-\ntranslation']
    accuracy = [100, 100, 83.3, 83.3]
    colors = [COLORS['success'], COLORS['primary'], COLORS['warning'], COLORS['danger']]
    
    bars = ax1.bar(methods, accuracy, color=colors, edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Precision@1 (%)', fontweight='bold')
    ax1.set_title('(a) Accuracy Comparison', fontweight='bold')
    ax1.set_ylim(0, 110)
    ax1.axhline(y=100, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Right: Latency comparison
    latency = [0.13, 0.11, 0.34, 1.14]
    bars2 = ax2.bar(methods, latency, color=colors, edgecolor='black', linewidth=1.2)
    ax2.set_ylabel('Response Time (seconds)', fontweight='bold')
    ax2.set_title('(b) Latency Comparison', fontweight='bold')
    ax2.set_ylim(0, 1.3)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                f'{height:.2f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.suptitle('Translation Strategy Evaluation (RQ1)', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_figure('fig1_translation_strategies')


def fig2_hybrid_retrieval():
    """Figure 2: Hybrid Retrieval Comparison (RQ2)"""
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    methods = ['Semantic\nOnly', 'BM25\nOnly', 'Hybrid\n70/30', 'Hybrid\n50/50', 'Cascade']
    p1 = [90, 52, 92, 86, 90]
    p3 = [94, 84, 98, 98, 94]
    p5 = [94, 88, 98, 98, 94]
    
    x = np.arange(len(methods))
    width = 0.25
    
    bars1 = ax.bar(x - width, p1, width, label='P@1', color=COLORS['primary'], 
                   edgecolor='black', linewidth=1)
    bars2 = ax.bar(x, p3, width, label='P@3', color=COLORS['secondary'],
                   edgecolor='black', linewidth=1)
    bars3 = ax.bar(x + width, p5, width, label='P@5', color=COLORS['success'],
                   edgecolor='black', linewidth=1)
    
    ax.set_ylabel('Accuracy (%)', fontweight='bold')
    ax.set_xlabel('Retrieval Method', fontweight='bold')
    ax.set_title('Hybrid Retrieval Performance Comparison (RQ2)', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend(loc='lower right', framealpha=0.9)
    ax.set_ylim(0, 105)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    # Highlight best method
    ax.axvline(x=2, color=COLORS['warning'], linestyle='--', linewidth=2, alpha=0.3)
    ax.text(2, 102, 'Best', ha='center', fontweight='bold', color=COLORS['warning'])
    
    plt.tight_layout()
    save_figure('fig2_hybrid_retrieval')


def fig3_robustness_analysis():
    """Figure 3: Robustness Analysis (RQ3)"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left: Category accuracy by query type
    query_types = ['Formal', 'Dialectal\nArabic', 'Short\nPhrases', 'Broken\nGrammar', 'Single\nWords']
    category_acc = [99, 90, 84, 80, 80]
    colors_left = [COLORS['success'], COLORS['primary'], COLORS['secondary'], 
                   COLORS['warning'], COLORS['danger']]
    
    bars1 = ax1.barh(query_types, category_acc, color=colors_left, 
                     edgecolor='black', linewidth=1.2)
    ax1.set_xlabel('Category Accuracy (%)', fontweight='bold')
    ax1.set_title('(a) Category Accuracy by Query Type', fontweight='bold')
    ax1.set_xlim(0, 105)
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars1, category_acc)):
        ax1.text(val + 1, i, f'{val}%', va='center', fontweight='bold')
    
    # Right: Source accuracy comparison (Formal vs Messy)
    metrics = ['P@1', 'P@3', 'P@5']
    formal_src = [84, 92, 94]
    messy_src = [51, 69, 78]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars2 = ax2.bar(x - width/2, formal_src, width, label='Formal Queries',
                    color=COLORS['success'], edgecolor='black', linewidth=1)
    bars3 = ax2.bar(x + width/2, messy_src, width, label='Messy Queries',
                    color=COLORS['danger'], edgecolor='black', linewidth=1)
    
    ax2.set_ylabel('Source Accuracy (%)', fontweight='bold')
    ax2.set_xlabel('Metric', fontweight='bold')
    ax2.set_title('(b) Exact Source Accuracy', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics)
    ax2.legend(loc='lower right', framealpha=0.9)
    ax2.set_ylim(0, 105)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bars in [bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{int(height)}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.suptitle('Robustness Analysis (RQ3)', fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    save_figure('fig3_robustness_analysis')


def fig4_system_comparison():
    """Figure 4: Overall System Performance & Ablation (RQ4)"""
    
    fig = plt.figure(figsize=(12, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    # Left: System vs Baseline comparison
    systems = ['Our System\n(Category)', 'Our System\n(Source)', 'BM25\nBaseline']
    accuracies = [99, 84, 56]
    colors_left = [COLORS['success'], COLORS['primary'], COLORS['neutral']]
    
    bars1 = ax1.bar(systems, accuracies, color=colors_left, 
                    edgecolor='black', linewidth=1.5, width=0.6)
    ax1.set_ylabel('Precision@1 (%)', fontweight='bold')
    ax1.set_title('(a) System vs Baseline', fontweight='bold')
    ax1.set_ylim(0, 110)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels and improvement
    for i, (bar, val) in enumerate(zip(bars1, accuracies)):
        ax1.text(bar.get_x() + bar.get_width()/2., val + 2,
                f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Show improvement
    ax1.annotate('', xy=(0, 99), xytext=(2, 56),
                arrowprops=dict(arrowstyle='<->', color=COLORS['warning'], lw=2))
    ax1.text(1, 77, '+43pp\n(77% gain)', ha='center', fontweight='bold',
            color=COLORS['warning'], fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['warning'], linewidth=2))
    
    # Right: Ablation study
    configs = ['Full\nSystem', 'Without\nKeyword\nBoosting', 'Without\nTitle\nMatching']
    ablation_acc = [99, 91, 99]
    impacts = [0, -8, 0]
    colors_right = [COLORS['success'], COLORS['warning'], COLORS['success']]
    
    bars2 = ax2.bar(configs, ablation_acc, color=colors_right,
                    edgecolor='black', linewidth=1.5, width=0.6)
    ax2.set_ylabel('Accuracy (%)', fontweight='bold')
    ax2.set_title('(b) Ablation Study (RQ4)', fontweight='bold')
    ax2.set_ylim(0, 110)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels and impact
    for i, (bar, val, impact) in enumerate(zip(bars2, ablation_acc, impacts)):
        ax2.text(bar.get_x() + bar.get_width()/2., val + 2,
                f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
        if impact != 0:
            ax2.text(bar.get_x() + bar.get_width()/2., val - 5,
                    f'{impact:+d}%', ha='center', va='top', fontweight='bold',
                    color='white', fontsize=10)
    
    plt.suptitle('System Performance & Component Analysis', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    save_figure('fig4_system_comparison')


if __name__ == "__main__":
    print("Generating publication-quality figures...")
    print("="*60)
    
    fig1_translation_strategies()
    fig2_hybrid_retrieval()
    fig3_robustness_analysis()
    fig4_system_comparison()
    
    print("="*60)
    print("✅ All figures generated successfully!")
    print("\nGenerated figures:")
    print("  - fig1_translation_strategies.{png,pdf}")
    print("  - fig2_hybrid_retrieval.{png,pdf}")
    print("  - fig3_robustness_analysis.{png,pdf}")
    print("  - fig4_system_comparison.{png,pdf}")
    print("\nTotal: 4 figures (8 files with PNG + PDF)")
