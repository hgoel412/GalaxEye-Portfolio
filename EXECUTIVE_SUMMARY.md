# EXECUTIVE SUMMARY: Maritime Surveillance Constellation Analysis

**Project:** GalaxEye-Aligned Multi-Sensor Constellation Study  
**Analyst:** Harshit Goel  
**Date:** December 2025  
**Tools:** STK 12.10 Pro, Python 3.11, Walker Constellation Design

---

## 🚀 Executive Overview

This independent research project analyzes the operational efficiency of **Walker constellations** for real-time surveillance of the **Indian Exclusive Economic Zone (EEZ)** and major ports. By processing **357,227 access windows** across 62 simulation scenarios, this study quantifies the precise trade-offs between coverage, revisit time, and constellation cost.

**Key Conclusion:** A **12-satellite constellation** utilizing **SAR+Optical Fusion** delivers the optimal operational balance, achieving **100% daily coverage** of all 5 major Indian ports and providing a **6.5x improvement** in surveillance capability compared to single-sensor architectures.

---

## 📊 Key Findings

### 1. The "Golden Ratio" Constellation (12 Satellites)
Analysis of coverage metrics reveals that the 12-satellite configuration is the "sweet spot" for commercial feasibility:
* **Operational Value:** Scaling from 6 to 12 satellites yields a **73% improvement** in EEZ coverage.
* **Diminishing Returns:** Expanding to 32 satellites adds only **22% marginal coverage** despite a **2.5x increase in cost**.
* **Recommendation:** The 12-satellite architecture provides 80% of the maximum theoretical operational value at approximately **50% of the cost** of a full 32-satellite dense shell.

### 2. Sensor Fusion: A Multiplicative Advantage
Integrating Synthetic Aperture Radar (SAR) with Optical sensors transforms the observation capability from additive to multiplicative:
* **Fusion Gain:** The combined sensor suite delivers a **6.5x coverage improvement** over SAR-only baselines.
* **Latency Reduction:** Multi-sensor tasking reduces detection latency from **15 minutes** (Optical only) to **4 minutes** (Fusion), enabling near real-time tracking.
* **Resilience:** The fusion approach ensures **24/7 all-weather capability**, overcoming the daylight limitations (14h max) of optical-only systems.

### 3. Port Surveillance & Ship Tracking
The simulation stress-tested surveillance performance over **Kandla, Mumbai, Kochi, Chennai, and Visakhapatnam**:
* **Port Access:** The 12-satellite constellation guarantees **100% daily coverage** for all 5 major ports.
* **Revisit Time:** Average revisit times were reduced to **2.1 hours** (down from 4.8 hours with 6 satellites), critical for monitoring moving vessels.
* **Tracking Continuity:** In transit scenarios, the system maintained continuous observation windows of up to **13.6 hours** for targets entering the West EEZ.

---

## 🛠️ Technical Methodology

The analysis pipeline was built to ensure reproducibility and high-fidelity simulation:

* **Simulation Engine:** **STK 12.10 Pro** was used to model orbital mechanics, employing **Walker Delta** patterns optimized for 51.6° inclination.
* **Data Pipeline:** A custom **Python 3.11** pipeline parsed **357,227 data points** from STK CSV exports to compute custom metrics like "Fusion Benefit" and "Detection Latency".
* **Validation:** All results were cross-verified against theoretical orbital period calculations to ensure physics compliance (zero missing values detected).
* **Visualization:** 7 professional dashboards were generated using **Matplotlib/Seaborn** to visualize complex temporal data.

---

## 🔮 Strategic Recommendations

Based on the quantitative analysis, the following deployment roadmap is recommended:

1.  **Phase 1 (Baseline):** Deploy the **12-satellite Walker constellation** to establish continuous port monitoring and <2.5h revisit capabilities.
2.  **Phase 2 (Augmentation):** Integrate **Optical payloads** to realize the 6.5x fusion multiplier and achieve all-weather dominance.
3.  **Phase 3 (Critical Ops):** Reserve the 32-satellite dense shell only for high-priority missions requiring **<10 minute** global revisit times.

---

*For full technical details, code, and dashboards, please refer to the accompanying GitHub repository.*
