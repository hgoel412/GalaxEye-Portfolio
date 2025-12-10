#!/usr/bin/env python3
"""
SATELLITE FUSION ANALYSIS - PHASE 2: METRICS COMPUTATION
=======================================================

Input:  parsed_passes.json (from Phase 1)
Output: 5 CSV results files for Phase 3 tables/visualizations
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any
import numpy as np

SCENARIO_START = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

def load_parsed_data() -> Dict[str, Any]:
    """Load Phase 1 output."""
    data_path = Path(r"D:\Job Portfolio\GalaxEye\parsed_data\parsed_passes.json")
    with open(data_path, 'r') as f:
        return json.load(f)

def compute_detection_latency(passes: list) -> float:
    """Time from scenario start to first pass (seconds)."""
    if not passes:
        return float('inf')
    first_pass = min(passes, key=lambda p: p['unix_start'])
    return first_pass['unix_start'] - SCENARIO_START.timestamp()

def compute_revisit_times(passes: list) -> dict:
    """Min/mean/max/median gaps between consecutive passes."""
    if len(passes) < 2:
        return {'min': float('inf'), 'mean': float('inf'), 'max': 0, 'median': float('inf')}
    
    # Sort by start time
    sorted_passes = sorted(passes, key=lambda p: p['unix_start'])
    gaps = []
    
    for i in range(len(sorted_passes)-1):
        gap = sorted_passes[i+1]['unix_start'] - sorted_passes[i]['unix_stop']
        if gap > 0:  # Only positive gaps
            gaps.append(gap)
    
    if not gaps:
        return {'min': 0, 'mean': 0, 'max': 0, 'median': 0}
    
    return {
        'min': min(gaps),
        'mean': np.mean(gaps),
        'max': max(gaps),
        'median': np.median(gaps),
        'count': len(gaps)
    }

def compute_fusion_windows(sar_passes: list, optical_passes: list) -> dict:
    """Count/duration of SAR+Optical overlaps."""
    if not sar_passes or not optical_passes:
        return {'count': 0, 'total_duration': 0, 'mean_duration': 0, 'max_duration': 0}
    
    overlaps = []
    sar_sorted = sorted(sar_passes, key=lambda p: p['unix_start'])
    opt_sorted = sorted(optical_passes, key=lambda p: p['unix_start'])
    
    for sar in sar_sorted:
        for opt in opt_sorted:
            overlap_start = max(sar['unix_start'], opt['unix_start'])
            overlap_end = min(sar['unix_stop'], opt['unix_stop'])
            
            if overlap_start < overlap_end:
                duration = overlap_end - overlap_start
                overlaps.append(duration)
    
    if not overlaps:
        return {'count': 0, 'total_duration': 0, 'mean_duration': 0, 'max_duration': 0}
    
    return {
        'count': len(overlaps),
        'total_duration': sum(overlaps),
        'mean_duration': np.mean(overlaps),
        'max_duration': max(overlaps)
    }

def compute_delivery_latency(ship_passes: list, gs_passes: list) -> dict:
    """Time from ship detection to nearest GS pass."""
    if not ship_passes or not gs_passes:
        return {'min': float('inf'), 'mean': float('inf'), 'max': float('inf')}
    
    latencies = []
    ship_sorted = sorted(ship_passes, key=lambda p: p['unix_stop'])
    gs_sorted = sorted(gs_passes, key=lambda p: p['unix_start'])
    
    for ship_pass in ship_sorted:
        ship_end = ship_pass['unix_stop']
        
        # Find nearest GS pass after ship pass ends
        candidates = [gs for gs in gs_sorted if gs['unix_start'] >= ship_end]
        if candidates:
            nearest = min(candidates, key=lambda gs: gs['unix_start'])
            latency = nearest['unix_start'] - ship_end
            latencies.append(latency)
    
    if not latencies:
        return {'min': float('inf'), 'mean': float('inf'), 'max': float('inf')}
    
    return {
        'min': min(latencies),
        'mean': np.mean(latencies),
        'max': max(latencies),
        'count': len(latencies)
    }

def main():
    print("=" * 80)
    print("SATELLITE FUSION ANALYSIS - PHASE 2: METRICS")
    print("=" * 80)
    
    # Load Phase 1 data
    data = load_parsed_data()
    results_dir = Path(r"D:\Job Portfolio\GalaxEye\results")
    results_dir.mkdir(exist_ok=True)
    
    # 1. DETECTION LATENCY
    detection_rows = []
    for ship in ['Ship1', 'Ship2', 'Ship3']:
        for const in [6, 12, 32]:
            sar_passes = data[ship]['SAR'].get(str(const), [])
            opt_passes = data[ship]['Optical'].get(str(const), [])
            
            sar_latency = compute_detection_latency(sar_passes)
            opt_latency = compute_detection_latency(opt_passes)
            fusion_latency = min(sar_latency, opt_latency)
            
            detection_rows.append({
                'ship': ship,
                'constellation': f"{const}-sat",
                'sar_latency_min': sar_latency/60,  # minutes
                'optical_latency_min': opt_latency/60,
                'fusion_latency_min': fusion_latency/60,
                'improvement_factor': sar_latency/fusion_latency if fusion_latency > 0 else 0
            })
    
    pd.DataFrame(detection_rows).to_csv(results_dir / "detection_latency_results.csv", index=False)
    
    # 2. REVISIT TIME (simplified - SAR vs Fusion)
    revisit_rows = []
    for ship in ['Ship1', 'Ship2', 'Ship3']:
        for const in [6, 12, 32]:
            sar_passes = data[ship]['SAR'].get(str(const), [])
            sar_opt_passes = sar_passes + data[ship]['Optical'].get(str(const), [])
            
            sar_revisit = compute_revisit_times(sar_passes)
            fusion_revisit = compute_revisit_times(sar_opt_passes)
            
            revisit_rows.append({
                'ship': ship,
                'constellation': f"{const}-sat",
                'sensor': 'SAR',
                **{k: v/3600 for k, v in sar_revisit.items() if k != 'count'}
            })
            revisit_rows.append({
                'ship': ship,
                'constellation': f"{const}-sat",
                'sensor': 'Fusion',
                **{k: v/3600 for k, v in fusion_revisit.items() if k != 'count'}
            })
    
    pd.DataFrame(revisit_rows).to_csv(results_dir / "revisit_time_results.csv", index=False)
    
    # 3. FUSION WINDOWS
    fusion_rows = []
    for ship in ['Ship1', 'Ship2', 'Ship3']:
        for const in [6, 12, 32]:
            sar_passes = data[ship]['SAR'].get(str(const), [])
            opt_passes = data[ship]['Optical'].get(str(const), [])
            windows = compute_fusion_windows(sar_passes, opt_passes)
            
            fusion_rows.append({
                'ship': ship,
                'constellation': f"{const}-sat",
                **windows
            })
    
    pd.DataFrame(fusion_rows).to_csv(results_dir / "fusion_windows_results.csv", index=False)
    
    print("✅ SAVED 3 results files:")
    print("   • detection_latency_results.csv")
    print("   • revisit_time_results.csv") 
    print("   • fusion_windows_results.csv")
    print("🚀 Ready for Phase 3 (Tables & Visualizations)")

if __name__ == "__main__":
    main()
