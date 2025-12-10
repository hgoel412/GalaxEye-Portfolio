#!/usr/bin/env python3
"""
SATELLITE FUSION ANALYSIS - PHASE 1 (COMMA-DELIMITED CSV FIX)
============================================================

FIX: Uses correct comma delimiter for STK CSV format
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# ========================================
# YOUR PATHS
# ========================================
DATA_DIR = Path(r"D:\Job Portfolio\GalaxEye\Raw Data")
OUTPUT_DIR = Path(r"D:\Job Portfolio\GalaxEye\parsed_data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_stk_csv(filepath: Path) -> List[Dict[str, Any]]:
    """Parse STK CSV (COMMA-DELIMITED with quoted headers)."""
    passes = []
    satellite_id = -1
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',')  # ✅ FIXED: Comma delimiter
        
        for row_num, row in enumerate(reader, 1):
            # Clean and skip empty rows
            row = [cell.strip().strip('"') for cell in row if cell.strip()]
            if not row or len(row) < 4:
                continue
            
            first_cell = row[0]
            
            # NEW SATELLITE: Header detection
            if (first_cell == 'Access' and 
                len(row) >= 4 and 
                'Start Time' in row[1]):
                satellite_id += 1
                print(f"DEBUG: New satellite {satellite_id} at line {row_num}")
                continue
            
            # SKIP STATISTICS ROWS
            if first_cell.startswith(('Min Duration', 'Max Duration', 
                                    'Mean Duration', 'Total Duration', 'Statistics')):
                continue
            
            # DATA ROW: Parse 1, "time", "time", duration
            try:
                access_id = int(first_cell)
                start_time = row[1].strip('"')
                stop_time = row[2].strip('"')
                duration = float(row[3].strip('"'))
                
                # Parse datetime
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
                
            except (ValueError, IndexError) as e:
                # Debug malformed rows
                if row_num < 20:  # Only show first 20 errors
                    print(f"DEBUG: Skip malformed row {row_num}: {row[:4]}")
                continue
    
    print(f"DEBUG: {filepath.name} → {len(passes)} passes, {satellite_id+1} satellites")
    return passes

def get_file_category(filename: str) -> tuple:
    """Map filename → (target, sensor, constellation)."""
    mapping = {
        # Ship1 (6)
        "Ship1-Constellation6_SAR_Access.csv": ("Ship1", "SAR", 6),
        "Ship1-Constellation6_Optical_Access.csv": ("Ship1", "Optical", 6),
        "Ship1-Constellation12_SAR_Access.csv": ("Ship1", "SAR", 12),
        "Ship1-Constellation12_Optical_Access.csv": ("Ship1", "Optical", 12),
        "Ship1-Constellation32_SAR_Access.csv": ("Ship1", "SAR", 32),
        "Ship1-Constellation32_Optical_Access.csv": ("Ship1", "Optical", 32),
        
        # Ship2 (6)
        "Ship2-Constellation6_SAR_Access.csv": ("Ship2", "SAR", 6),
        "Ship2-Constellation6_Optical_Access.csv": ("Ship2", "Optical", 6),
        "Ship2-Constellation12_SAR_Access.csv": ("Ship2", "SAR", 12),
        "Ship2-Constellation12_Optical_Access.csv": ("Ship2", "Optical", 12),
        "Ship2-Constellation32_SAR_Access.csv": ("Ship2", "SAR", 32),
        "Ship2-Constellation32_Optical_Access.csv": ("Ship2", "Optical", 32),
        
        # Ship3 (6)
        "Ship3-Constellation6_SAR_Access.csv": ("Ship3", "SAR", 6),
        "Ship3-Constellation6_Optical_Access.csv": ("Ship3", "Optical", 6),
        "Ship3-Constellation12_SAR_Access.csv": ("Ship3", "SAR", 12),
        "Ship3-Constellation12_Optical_Access.csv": ("Ship3", "Optical", 12),
        "Ship3-Constellation32_SAR_Access.csv": ("Ship3", "SAR", 32),
        "Ship3-Constellation32_Optical_Access.csv": ("Ship3", "Optical", 32),
        
        # Ground Stations (6)
        "GS_Ahmedabad-Walker6_Access.csv": ("groundstations", "Ahmedabad", 6),
        "GS_Ahmedabad-Walker12_Access.csv": ("groundstations", "Ahmedabad", 12),
        "GS_Ahmedabad-Walker32_Access.csv": ("groundstations", "Ahmedabad", 32),
        "GS_Sriharikota-Walker6_Access.csv": ("groundstations", "Sriharikota", 6),
        "GS_Sriharikota-Walker12_Access.csv": ("groundstations", "Sriharikota", 12),
        "GS_Sriharikota-Walker32_Access.csv": ("groundstations", "Sriharikota", 32),
    }
    return mapping.get(filename, (None, None, None))

def main():
    print("=" * 80)
    print("SATELLITE FUSION ANALYSIS - PHASE 1 (COMMA CSV FIXED)")
    print(f"📁 Reading: {DATA_DIR}")
    print(f"💾 Writing: {OUTPUT_DIR}")
    print("=" * 80)
    
    results = {}
    total_passes = 0
    total_duration = 0.0
    processed = 0
    
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    print(f"🔍 Found {len(csv_files)} CSV files\n")
    
    for filepath in csv_files:
        filename = filepath.name
        category = get_file_category(filename)
        
        if category[0] is None:
            print(f"ℹ️  SKIP {filename}")
            continue
        
        target, sensor, constellation = category
        
        # Initialize structure
        if target not in results: results[target] = {}
        if sensor not in results[target]: results[target][sensor] = {}
        
        # PARSE with debugging
        passes = parse_stk_csv(filepath)
        results[target][sensor][constellation] = passes
        
        file_passes = len(passes)
        file_duration = sum(p.get('duration_sec', 0) for p in passes)
        
        total_passes += file_passes
        total_duration += file_duration
        processed += 1
        
        status = "✅" if file_passes > 0 else "❌"
        print(f"{status} {filename:38s} | {file_passes:5d} passes | {file_duration:8.1f}s")
    
    # SUMMARY
    print("\n" + "=" * 80)
    print("✅ PHASE 1 RESULTS")
    print("=" * 80)
    print(f"📊 Files: {processed}/24")
    print(f"📈 Passes: {total_passes:,}")
    print(f"⏱️  Duration: {total_duration:,.1f}s ({total_duration/3600:.1f}h)")
    
    # SAVE
    output_path = OUTPUT_DIR / "parsed_passes.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, default=str, indent=2)
    
    print(f"\n💾 SAVED: {output_path}")
    print("🚀 Phase 2 ready!")

if __name__ == "__main__":
    main()
