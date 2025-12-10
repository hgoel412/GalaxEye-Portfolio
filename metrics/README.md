# Metrics & Analysis Results

All CSV files generated from STK access analysis pipeline.

## Files

### port_access_metrics.csv
Port surveillance metrics by constellation

**Columns:**
- Port name
- Constellation size (6/12/32)
- Coverage % (time visible)
- Revisit time (hours)
- Max passes/day
- Optical vs SAR comparison

### ship_transit_metrics.csv
Ship tracking capability

**Columns:**
- Ship ID
- Transit date
- Constellation size
- Total access windows
- Avg window duration
- Detection opportunities

### fusion_analysis_metrics.csv
SAR + Optical fusion benefits

**Columns:**
- Region
- SAR coverage %
- Optical coverage %
- Combined coverage %
- Fusion gain (factor)
- Revisit time improvement

### eez_sar_coverage.csv
EEZ-wide coverage statistics

**Columns:**
- Constellation size
- Coverage %
- Gap time (hours)
- Avg revisit time
- Monthly variation

### detection_latency_results.csv
Time from detection order to first observation

**Columns:**
- Target type (port/ship/EEZ)
- Constellation size
- Min latency (min)
- Avg latency (min)
- Max latency (min)

## Usage

```python
import pandas as pd

df = pd.read_csv('metrics/port_access_metrics.csv')
print(df.head())
print(df.describe())
