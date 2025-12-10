#!/usr/bin/env python3
"""
Parse EEZ SAR Access data only (no Optical - identical due to large EEZ areas).
Input: 6 EEZ SAR Access CSVs from Raw Data folder
Output: parsed_eez_sar_passes.json
"""

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

DATA_DIR = Path(r"D:\Job Portfolio\GalaxEye\Raw Data")
OUTPUT_DIR = Path(r"D:\Job Portfolio\GalaxEye\parsed_data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_stk_csv(filepath: Path) -> List[Dict[str, Any]]:
    """Parse STK CSV with stacked satellite blocks."""
    passes = []
    satellite_id = -1
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',')
        
        for row in reader:
            row = [cell.strip().strip('"') for cell in row if cell.strip()]
            if not row or len(row) < 4:
                continue
            
            first_cell = row[0]
            
            # NEW SATELLITE: Header row detected
            if (first_cell == 'Access' and len(row) >= 4 and 'Start Time' in row[1]):
                satellite_id += 1
                continue
            
            # SKIP STATISTICS ROWS
            if first_cell.startswith(('Min Duration', 'Max Duration', 'Mean Duration', 
                                     'Total Duration', 'Statistics')):
                continue
            
            # DATA ROW: Parse pass information
            try:
                access_id = int(first_cell)
                start_time = row[1].strip('"')
                stop_time = row[2].strip('"')
                duration = float(row[3].strip('"'))
                
                start_dt = datetime.strptime(start_time, "%d %b %Y %H:%M:%S.%f")
                stop_dt = datetime.strptime(stop_time, "%d %b %Y %H:%M:%S.%f")
                
                passes.append({
                    'satellite_id': satellite_id,
                    'pass_num': access_id,
                    'start_time_str': start_time,
                    'stop_time_str': stop_time,
                    'start_time': start_dt.isoformat(),
                    'stop_time': stop_dt.isoformat(),
                    'duration_sec': duration,
                    'unix_start': start_dt.timestamp(),
                    'unix_stop': stop_dt.timestamp()
                })
            except (ValueError, IndexError):
                continue
    
    return passes

def main():
    print("=" * 80)
    print("PARSING EEZ SAR ACCESS DATA")
    print("=" * 80)
    
    results = {}
    total_passes = 0
    
    # Expected files: EEZ_{West,East}-Constellation{6,12,32}_SAR_Access.csv
    csv_files = sorted(DATA_DIR.glob("EEZ_*_SAR_Access.csv"))
    
    if not csv_files:
        print("❌ No SAR Access files found in:", DATA_DIR)
        print("Looking for files matching: EEZ_*_SAR_Access.csv")
        return
    
    for filepath in csv_files:
        filename = filepath.name
        # Parse filename: EEZ_West-Constellation6_SAR_Access.csv
        # Remove .csv and EEZ_ prefix
        name_clean = filename.replace('.csv', '').replace('EEZ_', '')
        
        # Extract EEZ name (West or East - everything before the dash)
        eez_name = name_clean.split('-')[0]
        
        # Extract constellation number using regex
        match = re.search(r'Constellation(\d+)', filename)
        if not match:
            print(f"⚠️  SKIP {filename} - could not extract constellation number")
            continue
        const = int(match.group(1))
        
        if eez_name not in results:
            results[eez_name] = {}
        
        passes = parse_stk_csv(filepath)
        results[eez_name][const] = passes
        
        total_passes += len(passes)
        total_duration = sum(p['duration_sec'] for p in passes)
        
        print(f"✅ {filename:45s} | {len(passes):3d} passes | {total_duration:8.0f}s")
    
    print("\n" + "=" * 80)
    print(f"📊 Total passes: {total_passes:,}")
    
    output_path = OUTPUT_DIR / "parsed_eez_sar_passes.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, default=str, indent=2)
    
    print(f"💾 Saved: {output_path}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
