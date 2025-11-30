"""
Generate all visualizations from the notebook
Saves charts as PNG files in notebooks/figures/
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Create output directory
output_dir = Path('notebooks/figures')
output_dir.mkdir(exist_ok=True)

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

print("="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# 1. Overall System Performance
print("\n1. Generating Overall System Performance chart...")
metrics = {
    'Overall Accuracy': 96.0,
    'Arabic Accuracy': 96.0,
    'English Accuracy': 96.0,
    'Precision@3': 98.0,
    'Precision@5': 98.0
}

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(list(metrics.keys()), list(metrics.values()), color='#2E86AB')
ax.set_xlabel('Accuracy (%)', fontsize=12)
ax.set_title('System Performance Metrics', fontsize=14, fontweight='bold')
ax.set_xlim(0, 100)

for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
            f'{width:.1f}%', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '01_overall_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 01_overall_performance.png")

# 2. Category Performance
print("\n2. Generating Category Performance charts...")
categories = {
    'Business': (14, 14, 100),
    'Culture': (10, 10, 100),
    'Education': (16, 16, 100),
    'Health': (16, 16, 100),
    'Housing': (12, 12, 100),
    'Info': (10, 10, 100),
    'Transportation': (14, 14, 100),
    'Justice': (4, 8, 50)
}

cat_names = list(categories.keys())
accuracies = [v[2] for v in categories.values()]
queries = [v[1] for v in categories.values()]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Accuracy by category
colors = ['#A8DADC' if acc == 100 else '#E63946' for acc in accuracies]
bars1 = ax1.bar(cat_names, accuracies, color=colors)
ax1.set_ylabel('Accuracy (%)', fontsize=12)
ax1.set_title('Accuracy by Category', fontsize=14, fontweight='bold')
ax1.set_ylim(0, 110)
ax1.axhline(y=96, color='gray', linestyle='--', alpha=0.5, label='Overall Average')
ax1.legend()
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.0f}%', ha='center', va='bottom', fontweight='bold')

# Queries by category
bars2 = ax2.bar(cat_names, queries, color='#457B9D')
ax2.set_ylabel('Number of Queries', fontsize=12)
ax2.set_title('Test Queries by Category', fontsize=14, fontweight='bold')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
            f'{int(height)}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '02_category_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 02_category_performance.png")

# 3. Translation Strategies
print("\n3. Generating Translation Strategies comparison...")
strategies = {
    'Direct English': (100, 0.13),
    'Multilingual': (100, 0.11),
    'Translate + Embed': (83.3, 0.34),
    'Back-translation': (83.3, 1.14)
}

strategy_names = list(strategies.keys())
accuracies = [v[0] for v in strategies.values()]
times = [v[1] for v in strategies.values()]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Accuracy comparison
bars1 = ax1.bar(strategy_names, accuracies, color='#2A9D8F')
ax1.set_ylabel('Precision@1 (%)', fontsize=12)
ax1.set_title('Translation Strategy Accuracy', fontsize=14, fontweight='bold')
ax1.set_ylim(0, 110)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

# Response time comparison
bars2 = ax2.bar(strategy_names, times, color='#E76F51')
ax2.set_ylabel('Response Time (seconds)', fontsize=12)
ax2.set_title('Translation Strategy Latency', fontsize=14, fontweight='bold')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
            f'{height:.2f}s', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '03_translation_strategies.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 03_translation_strategies.png")

# 4. Hybrid Retrieval
print("\n4. Generating Hybrid Retrieval comparison...")
methods = {
    'Semantic Only': 84,
    'BM25 Only': 56,
    'Hybrid 70/30': 80,
    'Hybrid 50/50': 70,
    'Cascade': 84
}

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#06D6A0' if v >= 80 else '#EF476F' for v in methods.values()]
bars = ax.bar(list(methods.keys()), list(methods.values()), color=colors)
ax.set_ylabel('Precision@1 (%)', fontsize=12)
ax.set_title('Hybrid Retrieval Methods Comparison', fontsize=14, fontweight='bold')
ax.set_ylim(0, 100)
ax.axhline(y=84, color='gray', linestyle='--', alpha=0.5, label='Best Performance')
ax.legend()
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.0f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '04_hybrid_retrieval.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 04_hybrid_retrieval.png")

# 5. Ablation Study
print("\n5. Generating Ablation Study chart...")
configurations = {
    'Full System': 96.0,
    'Without Keyword\nBoosting': 89.0,
    'Without Title\nMatching': 96.0,
    'Pure Semantic\n(Baseline)': 89.0
}

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#118AB2' if v == 96 else '#FFB703' for v in configurations.values()]
bars = ax.bar(list(configurations.keys()), list(configurations.values()), color=colors)
ax.set_ylabel('Accuracy (%)', fontsize=12)
ax.set_title('Component Contribution (Ablation Study)', fontsize=14, fontweight='bold')
ax.set_ylim(0, 100)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

# Add contribution annotation
ax.annotate('', xy=(0.5, 96), xytext=(0.5, 89),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax.text(0.7, 92.5, '+7%\nKeyword\nBoosting', color='red', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '05_ablation_study.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 05_ablation_study.png")

# 6. System vs Baseline
print("\n6. Generating System vs Baseline comparison...")
comparison = {
    'Our System': 96.0,
    'BM25 Baseline': 56.0
}

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(list(comparison.keys()), list(comparison.values()), 
              color=['#06D6A0', '#EF476F'], width=0.6)
ax.set_ylabel('Accuracy (%)', fontsize=12)
ax.set_title('System Performance vs Baseline', fontsize=14, fontweight='bold')
ax.set_ylim(0, 110)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold')

# Add improvement annotation
ax.annotate('', xy=(0, 96), xytext=(0, 56),
            arrowprops=dict(arrowstyle='<->', color='blue', lw=3))
ax.text(-0.3, 76, '+40pp\n(71% relative)', color='blue', fontsize=12, fontweight='bold')

# Add statistical significance
ax.text(0.5, 102, 'p < 0.0001', ha='center', fontsize=11, 
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.tight_layout()
plt.savefig(output_dir / '06_system_vs_baseline.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 06_system_vs_baseline.png")

# 7. Response Time Analysis
print("\n7. Generating Response Time Analysis...")
components = {
    'Language\nDetection': 0.05,
    'Translation': 0.8,
    'Embedding': 0.1,
    'FAISS Search': 0.02,
    'LLM Generation': 2.1
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart
bars = ax1.barh(list(components.keys()), list(components.values()), color='#F4A261')
ax1.set_xlabel('Time (seconds)', fontsize=12)
ax1.set_title('Response Time Breakdown', fontsize=14, fontweight='bold')

for bar in bars:
    width = bar.get_width()
    ax1.text(width + 0.05, bar.get_y() + bar.get_height()/2,
            f'{width:.2f}s', ha='left', va='center', fontweight='bold')

# Pie chart
colors_pie = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51']
ax2.pie(list(components.values()), labels=list(components.keys()), autopct='%1.1f%%',
        colors=colors_pie, startangle=90)
ax2.set_title('Response Time Distribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '07_response_time.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 07_response_time.png")

print(f"\n   Total Response Time: {sum(components.values()):.2f}s")
print(f"   Average (without translation): {sum(components.values()) - 0.8:.2f}s")

# 8. Summary Statistics Table
print("\n8. Generating Summary Statistics table...")
summary_data = {
    'Metric': [
        'Overall Accuracy',
        'Arabic Accuracy',
        'English Accuracy',
        'Precision@3',
        'Precision@5',
        'MRR',
        'NDCG@5',
        'Response Time',
        'Statistical Significance'
    ],
    'Value': [
        '96.0% (96/100)',
        '96.0% (48/50)',
        '96.0% (48/50)',
        '98.0%',
        '98.0%',
        '0.970',
        '2.313',
        '0.16s average',
        'p < 0.0001'
    ]
}

df = pd.DataFrame(summary_data)

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=df.values, colLabels=df.columns,
                cellLoc='left', loc='center',
                colWidths=[0.5, 0.5])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Style header
for i in range(len(df.columns)):
    table[(0, i)].set_facecolor('#2E86AB')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(1, len(df) + 1):
    for j in range(len(df.columns)):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#F0F0F0')

plt.title('System Performance Summary', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(output_dir / '08_summary_statistics.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: 08_summary_statistics.png")

print("\n" + "="*80)
print("VISUALIZATION GENERATION COMPLETE")
print("="*80)
print(f"\nAll 8 visualizations saved to: {output_dir}/")
print("\nGenerated files:")
for i in range(1, 9):
    filename = list(output_dir.glob(f'0{i}_*.png'))[0].name
    print(f"  {i}. {filename}")
