# Technical Approach

## Data Source

- **STK 12.10 Pro** - Industry-standard satellite simulation software
- **Access Analysis** - 357,227+ data points from 62 STK scenario files
- **Geographic Coverage** - Indian maritime EEZ, 5 major ports, 3 sample ships

## Methodology

### 1. Constellation Design
- Walker constellation formulas
- 6, 12, 32 satellite configurations
- Incline 51.6°, optimized for Indian coverage

### 2. Data Extraction
- STK access windows (satellite-to-target visibility)
- Parsed CSV outputs containing:
  - Access start/end times
  - Maximum elevation angles
  - Duration windows
  - Line-of-sight constraints

### 3. Metrics Computation
- **Coverage %**: Time target is visible / Total time * 100
- **Revisit Time**: Average time between consecutive passes
- **Detection Latency**: Time from order to first detection
- **Fusion Benefit**: SAR + Optical combined coverage / SAR coverage

### 4. Visualization Pipeline
- CSV → Pandas DataFrame
- Analytics & aggregation
- Matplotlib/Seaborn rendering
- High-res JPG export (300 dpi)

## Key Assumptions

- Continuous satellite operation (no maintenance)
- All-weather SAR capability (24/7)
- Optical limited to daylight passes (14h/day avg)
- 5-min detection processing time
- 15-min ground station delivery latency

## Validation

- Cross-checked revisit times with Walker constellation theory
- Verified port coverage against STK's native reports
- Validated fusion logic against sensor constraint models
- Independent verification of 357K+ data points

## Tools & Languages

- **STK**: Access analysis, orbital mechanics
- **Python 3.11**: Data pipeline
- **Pandas**: CSV parsing & aggregation
- **Matplotlib**: Visualization
- **NumPy**: Numerical operations
