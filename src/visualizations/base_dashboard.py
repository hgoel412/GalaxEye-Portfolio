#!/usr/bin/env python3
"""
03_galaxeye_dashboard_fixed.py

GalaxEye Satellite Fusion Analysis - Fixed Dashboard

Reads Phase‑2 result CSVs:
    - detection_latency_results.csv
    - revisit_time_results.csv
    - fusion_windows_results.csv

Generates a 2x2 dashboard PNG with a correct, visible
'First Detection Latency' subplot.

Place this script in your `scripts` folder and ensure the
`results` folder contains the three CSV files.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------------------------------------------------------
# CONFIGURE PATHS
# ---------------------------------------------------------
# Base project directory (edit if needed)
BASE_DIR = Path(r"D:\Job Portfolio\GalaxEye")

RESULTS_DIR = BASE_DIR / "results"
OUT_DIR = RESULTS_DIR
OUT_DIR.mkdir(parents=True, exist_ok=True)

DET_FILE = RESULTS_DIR / "detection_latency_results.csv"
REV_FILE = RESULTS_DIR / "revisit_time_results.csv"
FUS_FILE = RESULTS_DIR / "fusion_windows_results.csv"
OUT_FIG = OUT_DIR / "GalaxEye_Dashboard_fixed.png"


def load_data():
    """Load all three Phase‑2 result tables."""
    detection = pd.read_csv(DET_FILE)
    revisit = pd.read_csv(REV_FILE)
    fusion = pd.read_csv(FUS_FILE)
    return detection, revisit, fusion


def fix_detection_latency(detection: pd.DataFrame) -> pd.DataFrame:
    """
    Fix negative latencies so the plot shows meaningful bars.

    The CSV has negative minutes because some first passes occur
    before the chosen scenario start time. To keep the *relative*
    differences while avoiding negative bars, shift all latency
    values per ship so that that ship’s earliest fusion latency
    becomes 0.
    """
    df = detection.copy()

    for ship in df["ship"].unique():
        mask = df["ship"] == ship
        min_fusion = df.loc[mask, "fusion_latency_min"].min()

        # Shift SAR, optical, and fusion latencies for this ship
        for col in ["sar_latency_min", "optical_latency_min", "fusion_latency_min"]:
            df.loc[mask, col] = df.loc[mask, col] - min_fusion

    # Clip any tiny negative numerical noise to 0
    df[["sar_latency_min", "optical_latency_min", "fusion_latency_min"]] = (
        df[["sar_latency_min", "optical_latency_min", "fusion_latency_min"]]
        .clip(lower=0)
    )

    return df


def build_dashboard(detection: pd.DataFrame,
                    revisit: pd.DataFrame,
                    fusion: pd.DataFrame) -> None:
    """Create and save the 4‑panel dashboard."""

    # Use seaborn theme
    sns.set_theme(style="whitegrid")

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("GalaxEye Satellite Fusion Analysis", fontsize=20, fontweight="bold")

    # -------------------------------------------------
    # Panel 1: Mean Revisit Time (Fusion)
    # -------------------------------------------------
    fusion_revisit = revisit[revisit["sensor"] == "Fusion"].copy()  # hours already
    ax = axes[0, 0]
    sns.barplot(
        data=fusion_revisit,
        x="constellation",
        y="mean",
        hue="ship",
        ax=ax,
    )
    ax.set_title("Mean Revisit Time (Fusion)\nLower is better", fontweight="bold")
    ax.set_ylabel("Hours")
    ax.set_xlabel("Constellation")
    ax.legend(title="Ship")

    # -------------------------------------------------
    # Panel 2: Fusion Windows Count
    # -------------------------------------------------
    ax = axes[0, 1]
    sns.barplot(
        data=fusion,
        x="constellation",
        y="count",
        hue="ship",
        ax=ax,
    )
    ax.set_title("SAR+Optical Fusion Windows\nOverlap opportunities per day",
                 fontweight="bold")
    ax.set_ylabel("Count")
    ax.set_xlabel("Constellation")
    ax.legend(title="Ship")

    # -------------------------------------------------
    # Panel 3: First Detection Latency (Fixed)
    # -------------------------------------------------
    fixed_detection = fix_detection_latency(detection)

    det_plot = fixed_detection.melt(
        id_vars=["ship", "constellation"],
        value_vars=["fusion_latency_min"],
        var_name="metric",
        value_name="minutes",
    )

    ax = axes[1, 0]
    sns.barplot(
        data=det_plot,
        x="constellation",
        y="minutes",
        hue="ship",
        ax=ax,
    )
    ax.set_title(
        "First Detection Latency (Relative)\n0 = earliest fusion per ship",
        fontweight="bold",
    )
    ax.set_ylabel("Minutes (relative to earliest per ship)")
    ax.set_xlabel("Constellation")
    ax.legend(title="Ship")

    # -------------------------------------------------
    # Panel 4: Multi‑Sensor Coverage (% of day)
    # -------------------------------------------------
    coverage = fusion.copy()
    # total_duration is in seconds → convert to percentage of 24h
    coverage["coverage_pct"] = coverage["total_duration"] / (24 * 3600) * 100.0

    ax = axes[1, 1]
    sns.barplot(
        data=coverage,
        x="constellation",
        y="coverage_pct",
        hue="ship",
        ax=ax,
    )
    ax.set_title(
        "Multi-Sensor Coverage (% of 24 h)\nTime with SAR+Optical overlap",
        fontweight="bold",
    )
    ax.set_ylabel("% of Day")
    ax.set_xlabel("Constellation")
    ax.legend(title="Ship")

    # -------------------------------------------------
    # Layout & Save
    # -------------------------------------------------
    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()
    print(f"✅ Dashboard saved to: {OUT_FIG}")


def main():
    print("=" * 80)
    print("GalaxEye Dashboard - Fixed First Detection Latency")
    print("=" * 80)
    detection, revisit, fusion = load_data()
    build_dashboard(detection, revisit, fusion)


if __name__ == "__main__":
    main()
