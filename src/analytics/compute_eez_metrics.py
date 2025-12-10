#!/usr/bin/env python3
"""
Compute EEZ SAR-only metrics:
  - Detection latency (time to first SAR pass over EEZ)
  - Revisit time (mean gap between consecutive SAR passes)
  - Coverage statistics
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

SCENARIO_START = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp()

DATA_DIR = Path(r"D:\Job Portfolio\GalaxEye\parsed_data")
RESULTS_DIR = Path(r"D:\Job Portfolio\GalaxEye\results")
RESULTS_DIR.mkdir(exist_ok=True)

def load_eez_sar_data():
    """Load parsed EEZ SAR passes."""
    with open(DATA_DIR / "parsed_eez_sar_passes.json", 'r') as f:
        return json.load(f)

def compute_detection_latency(passes: list) -> float:
    """Time from scenario start to first SAR pass (in minutes)."""
    if not passes:
        return float('inf')
    first = min(passes, key=lambda p: p['unix_start'])
    latency_sec = first['unix_start'] - SCENARIO_START
    return max(0, latency_sec / 60)  # Convert to minutes

def compute_revisit_times(passes: list) -> dict:
    """Compute min/mean/max/median gaps between consecutive passes."""
    if len(passes) < 2:
        return {
            'min': float('inf'),
            'mean': float('inf'),
            'max': 0,
            'median': float('inf'),
            'count': 0
        }
    
    sorted_passes = sorted(passes, key=lambda p: p['unix_start'])
    gaps = []
    
    for i in range(len(sorted_passes) - 1):
        gap = sorted_passes[i+1]['unix_start'] - sorted_passes[i]['unix_stop']
        if gap > 0:
            gaps.append(gap / 60)  # Convert to minutes
    
    if not gaps:
        return {
            'min': 0,
            'mean': 0,
            'max': 0,
            'median': 0,
            'count': 0
        }
    
    return {
        'min': min(gaps),
        'mean': np.mean(gaps),
        'max': max(gaps),
        'median': np.median(gaps),
        'count': len(gaps)
    }

def compute_total_access_time(passes: list) -> float:
    """Sum of all pass durations (in minutes)."""
    if not passes:
        return 0
    total_sec = sum(p['duration_sec'] for p in passes)
    return total_sec / 60

def compute_coverage_percent(passes: list) -> float:
    """Coverage as percentage of 24 hours."""
    total_min = compute_total_access_time(passes)
    total_24h_min = 24 * 60
    return (total_min / total_24h_min) * 100

def main():
    print("=" * 80)
    print("COMPUTING EEZ SAR METRICS")
    print("=" * 80)
    
    eez_data = load_eez_sar_data()
    
    # 1. DETECTION LATENCY
    print("\n📊 Detection Latency:")
    det_rows = []
    for eez in sorted(eez_data.keys()):
        for const in [6, 12, 32]:
            const_str = str(const)
            passes = eez_data[eez].get(const_str, [])
            latency = compute_detection_latency(passes)
            
            det_rows.append({
                'eez': eez,
                'constellation': f"{const}-sat",
                'detection_latency_min': latency,
                'num_passes': len(passes)
            })
            print(f"  {eez} {const}-sat: {latency:6.2f} min ({len(passes)} passes)")
    
    pd.DataFrame(det_rows).to_csv(RESULTS_DIR / "eez_sar_detection_latency.csv", index=False)
    print("  ✅ eez_sar_detection_latency.csv")
    
    # 2. REVISIT TIME
    print("\n📊 Revisit Time (mean):")
    rev_rows = []
    for eez in sorted(eez_data.keys()):
        for const in [6, 12, 32]:
            const_str = str(const)
            passes = eez_data[eez].get(const_str, [])
            rev = compute_revisit_times(passes)
            
            rev_rows.append({
                'eez': eez,
                'constellation': f"{const}-sat",
                'mean_revisit_min': rev['mean'],
                'min_revisit_min': rev['min'],
                'max_revisit_min': rev['max'],
                'median_revisit_min': rev['median'],
                'num_gaps': rev['count']
            })
            print(f"  {eez} {const}-sat: {rev['mean']:6.2f} min (min={rev['min']:.1f}, max={rev['max']:.1f})")
    
    pd.DataFrame(rev_rows).to_csv(RESULTS_DIR / "eez_sar_revisit_time.csv", index=False)
    print("  ✅ eez_sar_revisit_time.csv")
    
    # 3. COVERAGE STATISTICS
    print("\n📊 Coverage Statistics:")
    cov_rows = []
    for eez in sorted(eez_data.keys()):
        for const in [6, 12, 32]:
            const_str = str(const)
            passes = eez_data[eez].get(const_str, [])
            total_access = compute_total_access_time(passes)
            coverage_pct = compute_coverage_percent(passes)
            num_passes = len(passes)
            
            cov_rows.append({
                'eez': eez,
                'constellation': f"{const}-sat",
                'total_access_min': total_access,
                'coverage_percent': coverage_pct,
                'num_passes': num_passes,
                'avg_pass_duration_sec': np.mean([p['duration_sec'] for p in passes]) if passes else 0
            })
            print(f"  {eez} {const}-sat: {coverage_pct:5.2f}% ({total_access:.1f} min / {num_passes} passes)")
    
    pd.DataFrame(cov_rows).to_csv(RESULTS_DIR / "eez_sar_coverage.csv", index=False)
    print("  ✅ eez_sar_coverage.csv")
    
    print("\n" + "=" * 80)
    print("✅ All EEZ SAR metrics computed")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
