# NYC Motor Vehicle Crash Severity Analysis
## Night vs Day Comparison

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)]()

**Research Question**: Are motor vehicle crashes occurring during nighttime hours more severe (with higher average casualties) than those occurring during daytime hours in New York City?

**Conclusion**: ✅ **YES!** Nighttime crashes have significantly higher average casualties than daytime crashes (p < 0.0001)

---

## 📊 Key Findings

| Metric | Night (18:00-05:59) | Day (06:00-17:59) |
|--------|---------------------|-------------------|
| **Sample Size** | 346,547 | 657,312 |
| **Mean Casualties** | 0.3558 | 0.2654 |
| **Casualty Rate** | 23.73% | 18.68% |

**Statistical Test**: Welch's t-test, t(617,195) = 56.55, **p < 0.0001**  
**Effect Size**: Cohen's d = 0.1245 (small but significant)  
**Conclusion**: Nighttime crashes average **0.09 more casualties** per crash (34% higher)

---

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Analysis
```bash
# Statistical analysis
python scripts/quick_analysis.py

# Generate visualizations
python scripts/create_visualizations.py
```

### View Results
```bash
# View statistical results
cat results/analysis_results_quick.txt

# View figures
open figures/
```

---

## 📁 Project Structure

```
510 Project 2/
│
├── data/
│   ├── Motor_Vehicle_Collisions_-_Crashes.csv  (Raw data)
│   └── processed_data.csv                      (Analysis-ready) ⭐
│
├── scripts/
│   ├── data_clean.py              (Data cleaning)
│   ├── analysis.py                (Analysis module)
│   ├── statistical_tests.py       (Statistical tests)
│   ├── visualizations.py          (Visualization module)
│   ├── quick_analysis.py          (Quick analysis) ⭐
│   └── create_visualizations.py   (Generate figures) ⭐
│
├── results/
│   └── analysis_results_quick.txt (Statistical summary)
│
├── figures/                        (6 PNG visualizations)
│   ├── mean_comparison.png        ⭐
│   ├── hourly_patterns.png        ⭐
│   └── ... (4 more figures)
│
└── docs/
    ├── README.md                  (Detailed documentation)
    ├── PROJECT_SUMMARY.md         (Comprehensive summary)
    ├── report_template.md         (Report template)
    └── GIT_WORKFLOW.md            (Git workflow guide)
```

---

## 📊 Data Files

### processed_data.csv (Primary Data File)
- **Size**: 188 MB
- **Rows**: 1,003,859 crashes
- **Columns**: 25 (22 original + 3 derived)

**Original Columns (22)**:
- crash_date, crash_time, borough, zip_code
- street names, casualty counts (by type)
- contributing factors, vehicle types

**Derived Columns (3)**:
- `crash_hour`: Hour of day (0-23)
- `total_casualties`: Sum of injured + killed (DV)
- `time_period`: "Night" or "Day" classification (IV)

---

## 💻 Usage

### Rerun Complete Analysis
```bash
# Step 1: Statistical analysis
python scripts/quick_analysis.py
# Output: results/analysis_results_quick.txt

# Step 2: Generate visualizations
python scripts/create_visualizations.py
# Output: 6 PNG files in figures/
```

### Regenerate Data (if needed)
```bash
# Clean raw data
python scripts/data_clean.py

# Add derived variables
python scripts/analysis.py
```

---

## 📖 Documentation

### Getting Started
- **This README** - Complete overview and quick start guide ⭐
- `results/analysis_results_quick.txt` - Detailed statistical results

### For Report Writing
- `docs/report_template.md` - Complete report template (fill this out) ⭐⭐
- `figures/` - All 6 visualizations for your report

### For GitHub Collaboration
- `docs/GIT_WORKFLOW.md` - Step-by-step Git workflow guide ⭐

---

## 🎯 Deliverables

### 1. Written Report
- Template: `docs/report_template.md`
- Include results from `results/analysis_results_quick.txt`
- Insert figures from `figures/`

### 2. GitHub Repository
- ✅ All analysis scripts (modular design)
- ✅ Complete documentation
- ⏳ Create branches and Pull Requests (see `docs/GIT_WORKFLOW.md`)

### 3. Presentation (8 minutes)
- Use figures: `mean_comparison.png`, `hourly_patterns.png`
- Present key statistics and conclusions

---

## 🔬 Methodology Summary

### Variables
- **Independent Variable (IV)**: Time period (Night: 18:00-05:59, Day: 06:00-17:59)
- **Dependent Variable (DV)**: Total casualties per crash (injured + killed)

### Statistical Test
- **Test**: Welch's t-test (unequal variances)
- **Assumptions**: 
  - Independence: ✓ (verified by unique collision IDs)
  - Normality: ✓ (Central Limit Theorem applies, N > 300,000)
  - Homogeneity: ✗ (Levene's test p < 0.001, hence Welch's test)

### Results
- **t-statistic**: 56.55
- **p-value**: < 0.0001 (highly significant)
- **Cohen's d**: 0.1245 (small effect, but practically meaningful)
- **95% CI**: [0.0873, 0.0936]
- **Power**: 100% (sample size more than adequate)

---

## 💡 Key Insights

### Why Are Night Crashes More Severe?

Possible explanations:
1. **Reduced visibility** - Harder to detect hazards
2. **Alcohol involvement** - Higher DUI rates at night
3. **Driver fatigue** - More common during late hours
4. **Higher speeds** - Less traffic allows faster driving
5. **Reduced enforcement** - Fewer patrol units

### Policy Recommendations

1. **Enhanced nighttime lighting** - Prioritize high-crash corridors
2. **Increased DUI enforcement** - Focus on 22:00-04:00
3. **Public awareness campaigns** - Educate about nighttime risks
4. **Data-driven resource allocation** - Optimize EMS and police deployment

---

## 📦 Tech Stack

- **Language**: Python 3.8+
- **Data Processing**: pandas, numpy
- **Statistical Analysis**: scipy, statsmodels
- **Visualization**: matplotlib, seaborn
- **Data Source**: [NYC Open Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)

---

## 🎓 Academic Information

**Authors**: [Your Name], [Partner's Name]  
**Course**: Module Project 2 - Statistical Analysis  
**Date**: November 2024  
**Purpose**: Educational (University Course Assignment)

---

## 📞 Getting Help

| Question | Resource |
|----------|----------|
| How to start? | This README (Quick Start section) |
| Statistical details? | `results/analysis_results_quick.txt` |
| Complete overview? | `docs/PROJECT_SUMMARY.md` |
| How to write report? | `docs/report_template.md` |
| Git collaboration? | `docs/GIT_WORKFLOW.md` |
| Code questions? | Comments in Python scripts |

---

## 📄 License

This project is for educational use only. Data sourced from NYC Open Data.

---

## 🌟 Project Status

✅ Data processed (1M+ crashes)  
✅ Statistical analysis complete (p < 0.0001)  
✅ Visualizations generated (6 figures)  
✅ Documentation complete  
✅ Ready for report writing  
✅ Ready for GitHub submission  

---

**Last Updated**: October 23, 2024  
**Version**: 1.0
