#!/usr/bin/env python3
"""
Create EEZ SAR-only dashboard comparing West vs East EEZs across constellations.
Metrics: Detection latency, revisit time, coverage %.
"""

import pandas as pd
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
    
    # Create 2x2 dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("EEZ SAR Surveillance Analysis: West vs East", 
                 fontsize=16, fontweight="bold", y=0.995)
    
    # Panel 1: Detection Latency
    ax = axes[0, 0]
    sns.barplot(data=det, x='constellation', y='detection_latency_min', hue='eez', ax=ax)
    ax.set_title("First Detection Latency (SAR)", fontweight="bold")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Constellation")
    ax.legend(title="EEZ")
    
    # Panel 2: Mean Revisit Time
    ax = axes[0, 1]
    sns.barplot(data=rev, x='constellation', y='mean_revisit_min', hue='eez', ax=ax)
    ax.set_title("Mean Revisit Time (SAR)", fontweight="bold")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Constellation")
    ax.legend(title="EEZ")
    
    # Panel 3: Coverage %
    ax = axes[1, 0]
    sns.barplot(data=cov, x='constellation', y='coverage_percent', hue='eez', ax=ax)
    ax.set_title("SAR Coverage (% of 24 hours)", fontweight="bold")
    ax.set_ylabel("% of Day")
    ax.set_xlabel("Constellation")
    ax.legend(title="EEZ")
    
    # Panel 4: Number of Passes
    ax = axes[1, 1]
    sns.barplot(data=cov, x='constellation', y='num_passes', hue='eez', ax=ax)
    ax.set_title("Total SAR Passes per Day", fontweight="bold")
    ax.set_ylabel("Count")
    ax.set_xlabel("Constellation")
    ax.legend(title="EEZ")
    
    # Save
    plt.tight_layout()
    out_path = OUT_DIR / "EEZ_SAR_Dashboard.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print("=" * 80)
    print("✅ Dashboard saved: EEZ_SAR_Dashboard.png")
    print("=" * 80)

if __name__ == "__main__":
    main()
