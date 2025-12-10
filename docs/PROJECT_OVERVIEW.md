# GalaxEye Project Overview

## Mission
Design and analyze a satellite constellation for real-time maritime surveillance of the Indian Exclusive Economic Zone (EEZ) and major ports.

## What I Solved

### Problem
Traditional maritime surveillance is:
- Limited by earth station coverage
- Constrained by optical weather dependency
- Expensive at large scale

### Solution
**GalaxEye**: Multi-satellite constellation with SAR+Optical fusion providing:
- 24/7 coverage (all-weather SAR)
- Real-time port monitoring
- Ship tracking capability
- Cost-optimized constellation designs

## Key Results

| Constellation | Coverage | Revisit Time | Cost Efficiency |
|---------------|----------|--------------|-----------------|
| 6 satellites  | 7.2%     | 3-6 hours    | ✓✓✓             |
| 12 satellites | 12.5%    | 1-2 hours    | ✓✓              |
| 32 satellites | 15.3%    | 5-20 min     | ✓               |

## Technical Highlights

- **357,227 data points** from STK access analysis
- **7 professional dashboards** showing performance
- **SAR+Optical fusion** providing 6.5x coverage improvement
- **Production-ready code** with reproducible pipeline

## Technology

- STK 12.10 Pro (orbital mechanics)
- Python 3.11 (data pipeline)
- Pandas/NumPy (analytics)
- Matplotlib (visualization)

## What You'll Find Here

1. **`dashboards/`** - 7 visualizations of analysis
2. **`metrics/`** - 5 CSV files with detailed results
3. **`src/`** - Production Python code
4. **`docs/`** - Technical documentation
5. **`tests/`** - Unit tests for reproducibility

## Next Steps

- View dashboards in `dashboards/README.md`
- Run analysis: `python src/00_master_runner.py`
- Explore metrics in `metrics/`
- Check future work in `docs/FUTURE_WORK.md`
EOF
