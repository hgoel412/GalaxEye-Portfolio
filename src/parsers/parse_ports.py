#!/usr/bin/env python3
"""
Parse Port Access data (SAR + Optical, all constellations).
Ports: Mumbai, Chennai, Kochi, Kandla, Visakhapatnam
Constellations: Walker6, Walker12, Walker32
Sensors: SAR, Optical

Input: 30 port access CSV files
Output: parsed_port_access.json
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
    print("PARSING PORT ACCESS DATA (SAR + OPTICAL)")
    print("=" * 80)
    
    results = {}
    total_passes = 0
    
    # Expected files: Port_{PortName}-Walker{6,12,32}_{SAR,Optical}_Access.csv
    csv_files = sorted(DATA_DIR.glob("Port_*_Access.csv"))
    
    if not csv_files:
        print("❌ No port access files found in:", DATA_DIR)
        return
    
    for filepath in csv_files:
        filename = filepath.name
        # Parse filename: Port_Mumbai-Walker6_SAR_Access.csv
        
        # Extract port name
        port_match = re.search(r'Port_(\w+)', filename)
        if not port_match:
            print(f"⚠️  SKIP {filename} - could not extract port name")
            continue
        port_name = port_match.group(1)
        
        # Extract constellation (Walker6/12/32)
        const_match = re.search(r'Walker(\d+)', filename)
        if not const_match:
            print(f"⚠️  SKIP {filename} - could not extract constellation")
            continue
        const = int(const_match.group(1))
        
        # Extract sensor (SAR or Optical)
        sensor = "SAR" if "_SAR_" in filename else "Optical"
        
        if port_name not in results:
            results[port_name] = {}
        if sensor not in results[port_name]:
            results[port_name][sensor] = {}
        
        passes = parse_stk_csv(filepath)
        results[port_name][sensor][const] = passes
        
        total_passes += len(passes)
        total_duration = sum(p['duration_sec'] for p in passes)
        
        print(f"✅ {filename:50s} | {len(passes):3d} passes | {total_duration:8.0f}s")
    
    print("\n" + "=" * 80)
    print(f"📊 Total passes: {total_passes:,}")
    print(f"📍 Ports: {len(results)}")
    
    output_path = OUTPUT_DIR / "parsed_port_access.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, default=str, indent=2)
    
    print(f"💾 Saved: {output_path}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
