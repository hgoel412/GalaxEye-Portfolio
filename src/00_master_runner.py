
### `src/00_master_runner.py`

```python
"""
Master runner for GalaxEye portfolio analysis pipeline.

Orchestrates:
1. Data parsing (STK CSV files)
2. Metrics computation
3. Dashboard generation
"""

import sys
from pathlib import Path

# Import pipeline components
from src.parsers.parse_stk_access import parse_access_files
from src.analytics.coverage_analysis import compute_coverage_metrics
from src.analytics.fusion_analysis import compute_fusion_benefits
from src.visualizations.constellation_dashboard import create_constellation_dashboard
from src.visualizations.eez_dashboard import create_eez_dashboard
from src.visualizations.port_dashboard import create_port_dashboard
from src.visualizations.ship_transit_dashboard import create_ship_dashboard
from src.visualizations.multi_port_comparison import create_comparison_dashboard
from src.visualizations.fusion_dashboard import create_fusion_dashboard

def main():
    """Execute full analysis pipeline"""
    
    print("🛰️ GalaxEye Portfolio Analysis Pipeline")
    print("=" * 50)
    
    # 1. Parse data
    print("\n📊 Parsing STK access files...")
    access_data = parse_access_files()
    print(f"✓ Loaded {len(access_data)} access windows")
    
    # 2. Compute metrics
    print("\n📈 Computing coverage metrics...")
    metrics = compute_coverage_metrics(access_data)
    print("✓ Coverage analysis complete")
    
    # 3. Fusion analysis
    print("\n🔗 Computing fusion benefits...")
    fusion_metrics = compute_fusion_benefits(access_data)
    print("✓ Fusion analysis complete")
    
    # 4. Generate dashboards
    print("\n🎨 Generating visualizations...")
    create_constellation_dashboard()
    create_eez_dashboard()
    create_port_dashboard()
    create_ship_dashboard()
    create_comparison_dashboard()
    create_fusion_dashboard()
    print("✓ All dashboards generated")
    
    print("\n✅ Pipeline complete!")
    print("📁 Outputs saved to:")
    print("   - dashboards/")
    print("   - metrics/")

if __name__ == "__main__":
    main()
