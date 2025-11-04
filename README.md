# Paper Plane Flight Distance Analysis

A reproducible statistical analysis investigating the effect of paper plane size on flight distance.



## Quick Summary

**Research Question:** Does paper plane size significantly affect flight distance?

**Answer:** Yes. Paper plane size explains **91.7%** of variance in flight distance (F(14,135) = 106.09, p < 0.001, η² = 0.917).

**Key Finding:** Largest plane (13.18m) flew 18.6× farther than smallest plane (0.71m).



## Reproduction Instructions

Follow these steps to reproduce the entire analysis from scratch.

### Prerequisites

**Required Software:**
- Python 3.8 or higher
- pip package manager

**Required Python Packages:**
```bash
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

### Step 1: Install Dependencies

```bash
cd "/Users/leo/Desktop/510 Project 2"
pip install pandas numpy scipy matplotlib seaborn
```

Or create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy scipy matplotlib seaborn
```

### Step 2: Verify Data Files

Ensure the following data files exist in the `Data/` directory:

```
Data/
├── raw_flight_data.csv
└── processed_flights_data.csv
```

**Data file format:**

`raw_flight_data.csv` contains:
- `size_rank`: Paper plane size (1-15)
- `width_cm`: Paper width in cm
- `height_cm`: Paper height in cm
- `area_cm2`: Paper area in cm²
- `trial_number`: Trial number (1-10)
- `distance_m`: Flight distance in meters
- `timestamp`: Recording time
- `notes`: Trial notes

### Step 3: Run Data Processing (Optional)

If you need to regenerate processed data from raw data:

```bash
cd Script
python3 data_processing.py
```

**Expected output:**
```
Data Processing Script 
Input: ../Data/raw_flight_data.csv
Output: ../Data/processed_flights_data.csv

Step 1: Reading raw data...
Read 150 raw records

Step 2: Grouping by size...
Grouped into 15 sizes

Step 3: Calculating statistics...
  Size 1: 10 trials, mean = 13.18m
  Size 2: 10 trials, mean = 12.51m
  ...
  Size 15: 10 trials, mean = 0.71m

Processed 15 sizes

Step 4: Exporting processed data...
Data exported to: ../Data/processed_flights_data.csv

Processing Complete 
```

### Step 4: Run Statistical Analysis

Execute the complete statistical analysis:

```bash
cd Script
python3 statistical_analysis.py
```

**Expected output:**
```

PAPER PLANE FLIGHT DISTANCE ANALYSIS


1. DATA LOADING

Loaded data from: ../Data/raw_flight_data.csv
Total observations: 150
Number of size groups: 15
Trials per size: 10

2. HYPOTHESES

Null Hypothesis (H0):
  Paper plane size has no effect on flight distance.
  
Alternative Hypothesis (H1):
  Paper plane size affects flight distance.

Significance level: α = 0.05

3. DESCRIPTIVE STATISTICS


4. ASSUMPTION CHECKING
4.1 Normality Test (Shapiro-Wilk)
Result: 15/15 groups pass normality test (p > 0.05)

4.2 Homogeneity of Variance (Levene's Test)
Result: Unequal variances (p < 0.001)

5. ONE-WAY ANOVA
F-statistic: 106.0873
p-value: 0.000000
Decision: REJECT null hypothesis (p < 0.05)

6. EFFECT SIZE
Eta-squared (η²): 0.9167
Interpretation: large effect size

7. CORRELATION ANALYSIS
Correlation coefficient (r): -0.9240
p-value: 0.000001

8. POST-HOC ANALYSIS

9. CONFIDENCE INTERVALS
[95% CIs for each size]

10. SUMMARY OF FINDINGS
Key Results:
  • ANOVA F-statistic: 106.0873
  • p-value: 0.000000
  • Effect size (η²): 0.9167 (large)
  • Correlation (r): -0.9240

Statistical Conclusion:
  Paper plane size has a SIGNIFICANT effect on flight distance.
  
```

**Time to complete:** ~5 seconds

### Step 5: Generate Visualizations

Create all 10 figures for presentation and report:

```bash
cd Script
python3 create_visualizations.py
```

**Expected output:**
```

GENERATING VISUALIZATIONS FOR PRESENTATION

Loading data...
Loaded 150 observations

1. Creating bar chart: Mean distance by size...
   Saved: 01_mean_distance_by_size.png

2. Creating line plot: Distance trend with regression...
   Saved: 02_distance_trend.png

3. Creating scatter plot: Correlation analysis...
   Saved: 03_scatter_correlation.png

4. Creating box plot: Distribution by size...
   Saved: 04_boxplot_distribution.png

5. Creating error bar plot: Confidence intervals...
   Saved: 05_confidence_intervals.png

6. Creating variance comparison plot...
   Saved: 06_variance_comparison.png

7. Creating individual trials plot...
   Saved: 07_individual_trials.png

8. Creating effect size visualization...
   Saved: 08_effect_size.png

9. Creating pairwise comparison plot...
   Saved: 09_pairwise_comparisons.png

10. Creating size dimensions visualization...
   Saved: 10_size_dimensions.png

ALL VISUALIZATIONS SAVED TO: ../Figures/
```

**Time to complete:** ~10 seconds

**Output location:** All figures saved to `Figures/` directory as high-resolution PNG files (300 DPI).

### Step 6: Run Power Analysis (Optional)

To see the power analysis that justified sample size:

```bash
cd Script
python3 power_analysis_planner.py
```

**Expected output:**
```
 Settings 
alpha=0.050 (two-tailed), target power=0.80, CV=0.25
Number of sizes=15, planned n per group: n=10

Key Comparisons (Required n per group & Power at n=10
Size 5 vs 6: means=(6.73,4.56), Δ=2.17m, n_req≈7, power@n=10≈0.93
Size 1 vs 6: means=(13.18,4.56), Δ=8.62m, n_req≈2, power@n=10≈1.00
Size 14 vs 15: means=(1.74,0.71), Δ=1.03m, n_req≈2, power@n=10≈1.00
Size 3 vs 4: means=(7.44,7.48), Δ=0.04m, n_req≈34126, power@n=10≈0.05
```

---

## Project Structure

```
510 Project 2/
│
├── README.md
├── REPORT.md
│
├── Data/
│   ├── raw_flight_data.csv
│   └── processed_flights_data.csv
│
├── Script/
│   ├── data_collection.py
│   ├── data_processing.py
│   ├── statistical_analysis.py
│   ├── create_visualizations.py
│   └── power_analysis_planner.py
│
└── Figures/
    ├── 01_mean_distance_by_size.png
    ├── 02_distance_trend.png
    ├── 03_scatter_correlation.png
    ├── 04_boxplot_distribution.png
    ├── 05_confidence_intervals.png
    ├── 06_variance_comparison.png
    ├── 07_individual_trials.png
    ├── 08_effect_size.png
    ├── 09_pairwise_comparisons.png
    └── 10_size_dimensions.png
```



## Experimental Design Summary

### Variables

**Independent Variable:** Paper plane size
- 15 levels (Size 1 = largest, Size 15 = smallest)
- Size 1: US Letter (27.94 × 21.59 cm, area = 603.22 cm²)
- Each size: width and height reduced by 1 cm
- Size 15: 13.94 × 7.59 cm, area = 105.80 cm²

**Dependent Variable:** Flight distance (meters)

### Sample Size

- **n = 10** trials per size
- **N = 150** total observations (15 sizes × 10 trials)
- Justified by a priori power analysis (target power = 0.80, α = 0.05)

### Controls

- Same folding technique (standard dart fold)
- Same throwing method
- Indoor environment (minimal wind)
- Consistent measurement procedure

---

## Key Results

### Statistical Test Results

| Test | Result | Interpretation |
|------|--------|----------------|
| **One-way ANOVA** | F(14, 135) = 106.09, p < 0.001 | Highly significant |
| **Effect size** | η² = 0.917 | Large effect (91.7% variance explained) |
| **Correlation** | r = -0.924, p < 0.001 | Strong negative correlation |
| **R²** | 0.854 | 85.4% variance explained by linear trend |

### Descriptive Statistics

| Size | Mean (m) | SD (m) | 95% CI |
|------|----------|--------|--------|
| 1 (largest) | 13.18 | 2.56 | [11.35, 15.01] |
| 5 | 6.73 | 1.31 | [5.79, 7.67] |
| 10 | 2.53 | 0.49 | [2.18, 2.88] |
| 15 (smallest) | 0.71 | 0.14 | [0.61, 0.81] |

### Conclusion

**Paper plane size significantly affects flight distance**
- Null hypothesis rejected (p < 0.001)
- Large effect size (η² = 0.917)
- Strong linear relationship (r = -0.924)
- Smaller planes fly significantly shorter distances

---

## Troubleshooting

### Common Issues and Solutions

**Issue 1: ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution:** Install missing packages
```bash
pip install pandas numpy scipy matplotlib seaborn
```

**Issue 2: File not found error**
```
FileNotFoundError: [Errno 2] No such file or directory: '../Data/raw_flight_data.csv'
```
**Solution:** Ensure you're running scripts from the `Script/` directory
```bash
cd Script
python3 statistical_analysis.py
```

**Issue 3: Permission denied when saving figures**
```
PermissionError: [Errno 1] Operation not permitted
```
**Solution:** Check write permissions for `Figures/` directory
```bash
chmod -R 755 ../Figures/
```

**Issue 4: Matplotlib backend issues**
```
ImportError: Cannot load backend 'TkAgg'
```
**Solution:** Set matplotlib to use a different backend
```bash
export MPLBACKEND=Agg
python3 create_visualizations.py
```

---

## Verification Checklist

After running all scripts, verify the following outputs exist:

### Data Files
- [ ] `Data/raw_flight_data.csv` (150 rows)
- [ ] `Data/processed_flights_data.csv` (15 rows)

### Figures (all in `Figures/` directory)
- [ ] `01_mean_distance_by_size.png`
- [ ] `02_distance_trend.png`
- [ ] `03_scatter_correlation.png`
- [ ] `04_boxplot_distribution.png`
- [ ] `05_confidence_intervals.png`
- [ ] `06_variance_comparison.png`
- [ ] `07_individual_trials.png`
- [ ] `08_effect_size.png`
- [ ] `09_pairwise_comparisons.png`
- [ ] `10_size_dimensions.png`

### Expected Results
- [ ] ANOVA F-statistic ≈ 106.09
- [ ] p-value < 0.001
- [ ] Effect size (η²) ≈ 0.917
- [ ] Correlation (r) ≈ -0.924

---

## Quick Start (One Command)

To run the complete analysis pipeline:

```bash
cd Script && \
python3 data_processing.py && \
python3 statistical_analysis.py && \
python3 create_visualizations.py && \
echo "Analysis complete! Check Figures/ for visualizations."
```

**Total time:** ~20 seconds


## Documentation

### Complete Report

See `REPORT.md` for the full written report including:
- Background and motivation
- Detailed methodology
- Complete statistical results
- Interpretation and discussion
- Limitations
- Conclusions and recommendations
- References

### Script Documentation

Each Python script includes:
- Clear function definitions
- Step-by-step output messages
- Error handling
- Structured output format


## Data Description

### Raw Data Format (`raw_flight_data.csv`)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| size_rank | int | Size identifier (1-15) | 1 |
| width_cm | float | Paper width (cm) | 27.94 |
| height_cm | float | Paper height (cm) | 21.59 |
| area_cm2 | float | Paper area (cm²) | 603.22 |
| trial_number | int | Trial number (1-10) | 1 |
| distance_m | float | Flight distance (m) | 13.84 |
| timestamp | string | Recording time | 2025-11-01 22:57:44 |
| notes | string | Trial notes | Size 1 Trial 1 |

### Processed Data Format (`processed_flights_data.csv`)

| Column | Type | Description |
|--------|------|-------------|
| size_rank | int | Size identifier (1-15) |
| width_cm | float | Paper width (cm) |
| height_cm | float | Paper height (cm) |
| area_cm2 | float | Paper area (cm²) |
| mean_m | float | Mean flight distance (m) |
| trial_1 to trial_10 | float | Individual trial distances (m) |


## System Requirements

### Minimum Requirements
- **OS:** Windows 10, macOS 10.14+, or Linux
- **Python:** 3.8 or higher
- **RAM:** 2 GB
- **Storage:** 100 MB

### Recommended Requirements
- **OS:** macOS 11+, Windows 11, or Ubuntu 20.04+
- **Python:** 3.10 or higher
- **RAM:** 4 GB
- **Storage:** 500 MB

### Tested Environments
- macOS 14.0 (Sonoma) with Python 3.11
- Windows 11 with Python 3.10
- Ubuntu 22.04 with Python 3.10


## Citation

No AI tools were used during coding. ChatGPT and Gemini was only used for brainstorm.

If you use this analysis or methodology, please cite:

```
Hanfu Zhao, Jaideep Aher. (2025). Effect of Paper Plane Size on Flight Distance: 
A Statistical Analysis. AIPI 510, Duke University.
```


## Contact

**Author:** Hanfu Zhao, Jaideep Aher

## License

This project is provided for educational purposes. All code and documentation are available for academic use with proper attribution.


**Last Updated:** November 2, 2025

**Reproducibility Status:** Fully reproducible

**Estimated Time to Reproduce:** 20-30 minutes (including installation)
