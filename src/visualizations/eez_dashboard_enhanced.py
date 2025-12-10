#!/usr/bin/env python3
"""
Enhanced EEZ SAR dashboard with:
  1. 5th panel: Cost-benefit tradeoff (revisit improvement per satellite)
  2. Threshold annotations on revisit plot (60 min acceptable, 30 min target)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

RESULTS_DIR = Path(r"D:\Job Portfolio\GalaxEye\results")
OUT_DIR = Path(r"D:\Job Portfolio\GalaxEye\visualizations")
OUT_DIR.mkdir(exist_ok=True)

def main():
    # Load data
    det = pd.read_csv(RESULTS_DIR / "eez_sar_detection_latency.csv")
    rev = pd.read_csv(RESULTS_DIR / "eez_sar_revisit_time.csv")
    cov = pd.read_csv(RESULTS_DIR / "eez_sar_coverage.csv")
    
    # Set style
    sns.set_theme(style="whitegrid")
    
    # Create 2x3 dashboard (6 panels instead of 4)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("EEZ SAR Surveillance Analysis: West vs East - Enhanced", 
                 fontsize=16, fontweight="bold", y=0.995)
    
    # ===== Panel 1: Detection Latency =====
    ax = axes[0, 0]
    sns.barplot(data=det, x='constellation', y='detection_latency_min', hue='eez', ax=ax)
    ax.set_title("First Detection Latency (SAR)", fontweight="bold")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Constellation")
    ax.legend(title="EEZ")
    
    # ===== Panel 2: Mean Revisit Time with THRESHOLDS =====
    ax = axes[0, 1]
    sns.barplot(data=rev, x='constellation', y='mean_revisit_min', hue='eez', ax=ax)
    
    # Add threshold lines
    ax.axhline(y=60, color='orange', linestyle='--', linewidth=2, label='60 min acceptable', alpha=0.7)
    ax.axhline(y=30, color='red', linestyle='--', linewidth=2, label='30 min target', alpha=0.7)
    
    ax.set_title("Mean Revisit Time (SAR) with Thresholds", fontweight="bold")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Constellation")
    ax.legend(loc='upper right', fontsize=9)
    ax.set_ylim([0, max(rev['mean_revisit_min'].max(), 80)])
    
    # ===== Panel 3: Coverage % =====
    ax = axes[0, 2]
    sns.barplot(data=cov, x='constellation', y='coverage_percent', hue='eez', ax=ax)
    ax.set_title("SAR Coverage (% of 24 hours)", fontweight="bold")
    ax.set_ylabel("% of Day")
    ax.set_xlabel("Constellation")
    ax.legend(title="EEZ")
    
    # ===== Panel 4: Number of Passes =====
    ax = axes[1, 0]
    sns.barplot(data=cov, x='constellation', y='num_passes', hue='eez', ax=ax)
    ax.set_title("Total SAR Passes per Day", fontweight="bold")
    ax.set_ylabel("Count")
    ax.set_xlabel("Constellation")
    ax.legend(title="EEZ")
    
    # ===== Panel 5: Cost-Benefit Tradeoff (NEW) =====
    ax = axes[1, 1]
    
    # Compute improvement per satellite for each EEZ
    improvement_data = []
    for eez in sorted(rev['eez'].unique()):
        eez_rev = rev[rev['eez'] == eez].sort_values('constellation')
        
        # Extract constellation numbers and revisit times
        consts = [6, 12, 32]
        revisits = []
        for c in consts:
            rv = eez_rev[eez_rev['constellation'] == f"{c}-sat"]['mean_revisit_min'].values
            if len(rv) > 0:
                revisits.append(rv[0])
        
        # Calculate improvement per additional satellite
        if len(revisits) >= 2:
            improvement_6to12 = (revisits[0] - revisits[1]) / (12 - 6)  # min reduction per satellite
            improvement_12to32 = (revisits[1] - revisits[2]) / (32 - 12)
            
            improvement_data.append({
                'eez': eez,
                'phase': '6→12 sat',
                'improvement_per_sat': improvement_6to12,
                'constellation_range': '6-12'
            })
            improvement_data.append({
                'eez': eez,
                'phase': '12→32 sat',
                'improvement_per_sat': improvement_12to32,
                'constellation_range': '12-32'
            })
    
    improvement_df = pd.DataFrame(improvement_data)
    sns.barplot(data=improvement_df, x='phase', y='improvement_per_sat', hue='eez', ax=ax)
    ax.set_title("Revisit Improvement per Added Satellite", fontweight="bold")
    ax.set_ylabel("Minutes reduction per satellite")
    ax.set_xlabel("Constellation Phase")
    ax.legend(title="EEZ")
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', fontsize=9)
    
    # ===== Panel 6: Constellation Recommendation Matrix =====
    ax = axes[1, 2]
    ax.axis('off')
    
    # Create recommendation text
    recommendation_text = """
CONSTELLATION RECOMMENDATIONS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target: 30 min revisit
  • West EEZ: 12-sat required ✓
  • East EEZ: 12-sat required ✓

Target: 60 min revisit
  • West EEZ: 6-sat sufficient ✓
  • East EEZ: 6-sat marginal ~

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Business Case (32-sat):
  • 5-7× improvement in revisit
  • Continuous monitoring capability
  • ROI: High for critical coverage
  
Efficient Choice (12-sat):
  • 2-3× improvement over 6-sat
  • Cost-effective for most ops
  • Meets 30 min target both EEZs
"""
    
    ax.text(0.05, 0.95, recommendation_text, 
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Save
    plt.tight_layout()
    out_path = OUT_DIR / "EEZ_SAR_Dashboard_Enhanced.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print("=" * 80)
    print("✅ Enhanced dashboard saved: EEZ_SAR_Dashboard_Enhanced.png")
    print("=" * 80)
    print("\n📊 Dashboard features:")
    print("   1. Threshold annotations (60 min acceptable, 30 min target)")
    print("   2. Cost-benefit analysis (improvement per satellite)")
    print("   3. Constellation recommendation matrix")
    print("=" * 80)

if __name__ == "__main__":
    main()
