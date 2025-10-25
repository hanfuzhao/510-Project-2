# Statistical Analysis Report: Night vs Day Motor Vehicle Crash Severity in NYC

**Authors:** [Your Name], [Partner's Name]  
**Course:** [Course Number and Name]  
**Date:** November 4, 2024

---

## Abstract

**[150-250 words summarizing the entire study]**

This study investigates whether motor vehicle crashes occurring during nighttime hours are more severe than those occurring during daytime in New York City. Using a dataset of [N] crashes from the NYC Open Data portal spanning [date range], we classified crashes into Night (18:00-05:59) and Day (06:00-17:59) groups and compared mean casualties per crash (injured + killed). An independent samples t-test revealed [significant/no significant] difference between groups (t = [value], p = [value], Cohen's d = [value]). [State main finding and practical implication in 1-2 sentences]. These findings [suggest/do not suggest] that time of day is associated with crash severity in NYC, with implications for [traffic safety policy/public awareness/resource allocation].

---

## 1. Background & Motivation

### 1.1 Context

Motor vehicle crashes are a leading cause of injury and death in urban environments. Understanding factors that contribute to crash severity is crucial for developing effective traffic safety interventions. Time of day represents a potentially important but understudied factor in crash severity.

### 1.2 Why This Matters

**[Explain the practical and theoretical importance of your research question]**

- **Public Safety:** [Discuss implications for traffic safety]
- **Resource Allocation:** [Discuss how findings could inform police patrol, EMS deployment]
- **Policy Development:** [Discuss potential interventions - lighting, speed limits, DUI checkpoints]
- **Existing Research:** [Briefly mention what is known about this topic, if anything]

### 1.3 Research Question

**Are motor vehicle crashes occurring during nighttime hours (18:00-05:59) more severe, as measured by total casualties per crash, than crashes occurring during daytime hours (06:00-17:59) in New York City?**

### 1.4 Rationale for Time Period Classification

We define:
- **Night:** 18:00 (6 PM) to 05:59 (6 AM) - periods of reduced visibility
- **Day:** 06:00 (6 AM) to 17:59 (6 PM) - periods of better visibility

**Justification:** [Explain why this classification makes sense - visibility, traffic patterns, driver behavior]

Factors that may differ between night and day:
- Visibility and lighting conditions
- Traffic density and congestion
- Alcohol consumption patterns
- Driver fatigue levels
- Speed and driving behaviors
- Law enforcement presence

---

## 2. Hypotheses

### 2.1 Null Hypothesis (H₀)

**H₀:** μ_night = μ_day

There is no difference in mean total casualties per crash between nighttime and daytime motor vehicle crashes in NYC.

### 2.2 Alternative Hypothesis (H₁)

**H₁:** μ_night ≠ μ_day

There is a difference in mean total casualties per crash between nighttime and daytime motor vehicle crashes in NYC.

### 2.3 Directional Prediction (Exploratory)

**[Optional: State your predicted direction and reasoning]**

We tentatively predict that nighttime crashes may be more severe because:
- Reduced visibility increases reaction times
- Higher prevalence of impaired driving (alcohol/drugs)
- Higher speeds due to lower traffic density
- Driver fatigue is more common

However, daytime crashes could also be more severe due to:
- Higher traffic density increases multi-vehicle collisions
- More pedestrians and cyclists present
- [Other factors]

We use a **two-tailed test** to remain open to either direction.

---

## 3. Experimental Design

### 3.1 Study Type

**Quasi-Experimental Observational Study**

This is not a true experiment because we cannot randomly assign crashes to occur at night or during the day. Instead, we use existing observational data and classify crashes based on their naturally occurring time.

### 3.2 Variables

**Independent Variable (IV):**
- **Variable:** Time period
- **Levels:** Night (18:00-05:59), Day (06:00-17:59)
- **Type:** Categorical, binary
- **Measurement:** Extracted from crash_time field

**Dependent Variable (DV):**
- **Variable:** Total casualties per crash
- **Definition:** Sum of number_of_persons_injured + number_of_persons_killed
- **Type:** Continuous (count data)
- **Scale:** 0 to maximum observed casualties
- **Measurement:** Recorded by NYPD officers at crash scene

### 3.3 Control Conditions

To minimize confounding, our data:
- Comes from a **single city** (NYC) - controls for geographic factors
- Covers a **consistent time period** - controls for temporal trends
- Uses a **single data source** (NYPD crash reports) - controls for measurement consistency
- Includes **only complete records** (no missing data) - reduces bias

**Limitations in control:**
- Cannot control for weather, traffic conditions, driver characteristics, or other crash-specific factors
- No random assignment to groups

### 3.4 Randomization

**Not applicable** - this is observational data. Crashes occur naturally and are classified post-hoc based on time.

### 3.5 Data Source

- **Source:** NYC Open Data - Motor Vehicle Collisions (Crashes)
- **URL:** https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
- **Coverage:** [Specify date range of your data]
- **Original N:** [Original number of records]
- **Final N after cleaning:** [Final number of records]

---

## 4. Power Analysis

### 4.1 Purpose

Power analysis serves two purposes:
1. **A priori:** Determine necessary sample size (not applicable here - we use existing data)
2. **Post hoc:** Assess whether our sample provides adequate power to detect meaningful effects

### 4.2 Assumptions

- **Significance level (α):** 0.05 (two-tailed)
- **Desired power:** 0.80 (80% probability of detecting a true effect)
- **Effect size:** 
  - Small effect: Cohen's d = 0.2
  - Medium effect: Cohen's d = 0.5
  - Observed effect: d = [calculate from your data]

### 4.3 Sample Size Calculation

**Using statsmodels.stats.power.TTestIndPower:**

For a two-sample t-test with α = 0.05 and power = 0.80:

| Effect Size (Cohen's d) | Required N per Group |
|-------------------------|----------------------|
| Small (0.2)            | [Calculate]          |
| Medium (0.5)           | [Calculate]          |
| Large (0.8)            | [Calculate]          |

**Our actual sample sizes:**
- Night group: N = [XXX,XXX]
- Day group: N = [XXX,XXX]

**Conclusion:** [State whether you have adequate power]

### 4.4 Achieved Power

Given our actual sample sizes and observed effect size (d = [XXX]), our achieved power is [XXX]%.

**Interpretation:** [Explain what this means for your ability to detect effects]

### 4.5 Minimum Detectable Effect (MDE)

With our sample sizes and 80% power, the minimum effect we can reliably detect is Cohen's d = [XXX].

**Practical significance:** [Discuss whether this MDE represents a practically meaningful difference]

### 4.6 Software Used

```python
from statsmodels.stats.power import TTestIndPower
power_analyzer = TTestIndPower()
```

---

## 5. Data Collection & Cleaning

### 5.1 Data Collection

**Source:** NYC Open Data portal, accessed [date]

**Collection method:** Downloaded CSV file containing all reported motor vehicle crashes in NYC.

**Variables collected:**
- crash_date, crash_time
- Location information (borough, street names, coordinates)
- Casualty counts (injured/killed by type: persons, pedestrians, cyclists, motorists)
- Contributing factors
- Vehicle types

### 5.2 Data Cleaning Procedures

**Script:** `data_clean.py`

**Steps:**
1. **Loaded raw data:** N = [original count] records
2. **Standardized column names:** Converted to lowercase with underscores
3. **Dropped irrelevant columns:** [List columns dropped]
4. **Handled missing values:**
   - Removed records with missing data in key fields (crash_date, crash_time, casualty counts)
   - Kept records with missing vehicle type codes (non-essential)
5. **Converted data types:**
   - crash_date to datetime
   - casualty counts to numeric
6. **Sorted data:** By crash_date and crash_time (chronological order)
7. **Saved cleaned data:** `cleaned_final.csv`, N = [final count] records

**Data quality checks:**
- Verified no duplicate collision IDs
- Checked for impossible values (e.g., negative casualties)
- Confirmed date ranges are reasonable

### 5.3 Data Processing for Analysis

**Script:** `analysis.py`

**Derived variables:**
1. **crash_hour:** Extracted hour (0-23) from crash_time
2. **time_period:** Classified as "Night" (18:00-05:59) or "Day" (06:00-17:59)
3. **total_casualties:** Sum of number_of_persons_injured + number_of_persons_killed

**Final dataset:** `processed_data.csv`

---

## 6. Statistical Analysis

### 6.1 Descriptive Statistics

**Table 1: Descriptive Statistics by Time Period**

| Statistic | Night (18:00-05:59) | Day (06:00-17:59) |
|-----------|---------------------|-------------------|
| N         | [XXX,XXX]           | [XXX,XXX]         |
| Mean      | [X.XXXX]            | [X.XXXX]          |
| Std Dev   | [X.XXXX]            | [X.XXXX]          |
| Median    | [X.XX]              | [X.XX]            |
| Q1        | [X.XX]              | [X.XX]            |
| Q3        | [X.XX]              | [X.XX]            |
| Min       | [X]                 | [X]               |
| Max       | [X]                 | [X]               |

**Mean difference (Night - Day):** [X.XXXX] casualties per crash

**[Insert Figure 1: Distribution comparison plots here]**

**Observations:**
- [Describe the shape of distributions]
- [Comment on any skewness or outliers]
- [Describe the difference in central tendency]

### 6.2 Assumption Checks

#### 6.2.1 Independence

**Assumption:** Observations are independent of one another.

**Assessment:** 
- Each row represents a unique crash event (verified by collision_id)
- Crashes are unlikely to be directly causally related to one another
- **✓ Assumption satisfied**

#### 6.2.2 Normality

**Assumption:** Data in each group are approximately normally distributed (or n is large enough for Central Limit Theorem to apply).

**Assessment:**

**Shapiro-Wilk Test (on samples of 5000):**
- Night: W = [X.XXXX], p = [X.XXXX]
- Day: W = [X.XXXX], p = [X.XXXX]

**[Insert Figure 2: Q-Q plots here]**

**Interpretation:**
- [Discuss whether data are normally distributed]
- With n > 30,000 in each group, the Central Limit Theorem applies
- The t-test is robust to violations of normality with large samples
- **Conclusion:** [Can/Cannot] proceed with t-test

#### 6.2.3 Homogeneity of Variance

**Assumption:** Variances in the two groups are approximately equal.

**Levene's Test:**
- Test statistic: [X.XXXX]
- p-value: [X.XXXX]

**Interpretation:**
- If p < 0.05: Variances are significantly different → use **Welch's t-test**
- If p ≥ 0.05: Variances are approximately equal → use standard t-test

**Decision:** [State which test will be used and why]

### 6.3 Hypothesis Test

**Test:** Independent Samples t-test (two-tailed)
- If variances are equal: Standard t-test
- If variances are unequal: Welch's t-test

**Script:** `statistical_tests.py`

**Results:**

**Test Statistics:**
- t-statistic: [X.XXXX]
- Degrees of freedom: [XXXX.XX]
- p-value: [X.XXXXXX]

**95% Confidence Interval for Mean Difference:**
- [X.XXXX, X.XXXX]

**Effect Size:**
- Cohen's d: [X.XXXX]
- Interpretation: [Negligible/Small/Medium/Large] effect

**[Insert Figure 3: Statistical results visualization here]**

### 6.4 Decision

**Using α = 0.05:**

**[Choose one:]**

✓ **REJECT H₀** (if p < 0.05)
- The p-value ([X.XXXX]) is less than our significance level (0.05)
- We have sufficient evidence to conclude that mean casualties per crash differ between night and day
- [State direction: Night crashes are more/less severe than day crashes]
- The mean difference is [X.XX] casualties per crash, 95% CI [X.XX, X.XX]

**OR**

✗ **FAIL TO REJECT H₀** (if p ≥ 0.05)
- The p-value ([X.XXXX]) is greater than our significance level (0.05)
- We do not have sufficient evidence to conclude that mean casualties differ between night and day
- Any observed difference could reasonably be due to chance

---

## 7. Interpretation of Results

### 7.1 Statistical Significance

**[Interpret your p-value and what it means]**

Our analysis [found/did not find] a statistically significant difference in crash severity between night and day (p = [X.XXX]). This means that [explain in plain language].

### 7.2 Practical Significance

**Effect Size Interpretation:**

Cohen's d = [X.XX], which represents a **[small/medium/large]** effect size.

**What this means in practice:**
- The average crash during [night/day] results in [X.XX] more casualties than during [day/night]
- This represents a [X]% [increase/decrease] in average casualties
- [Discuss whether this is practically meaningful for traffic safety policy]

### 7.3 Confidence Interval

The 95% confidence interval for the mean difference is [[X.XX], [X.XX]].

**Interpretation:**
- We are 95% confident that the true mean difference in casualties per crash between night and day falls within this range
- [Comment on whether the interval includes zero, and what that means]
- [Discuss the precision of the estimate]

### 7.4 Exploratory: Hourly Patterns

**[Optional: Include analysis of hourly patterns]**

**[Insert Figure 4: Hourly crash severity patterns here]**

Looking at crash severity by individual hour reveals:
- [Describe any patterns observed]
- [Comment on peak severity hours]
- [Discuss any surprises or interesting findings]

---

## 8. Limitations

### 8.1 Study Design Limitations

1. **Observational, not experimental**
   - Cannot establish causation, only association
   - Many potential confounding variables are uncontrolled

2. **Quasi-experimental design**
   - No random assignment to groups
   - Time of crash is self-selected (by drivers' schedules, circumstances)

### 8.2 Confounding Variables

Factors that may differ between night and day crashes and could affect severity:

| Potential Confounder | Expected Pattern | Impact on Results |
|----------------------|------------------|-------------------|
| Traffic density      | Higher during day | [Discuss] |
| Alcohol involvement  | Higher at night | [Discuss] |
| Speed               | Higher at night | [Discuss] |
| Visibility          | Lower at night | [Discuss] |
| Driver fatigue      | Higher at night | [Discuss] |
| Weather conditions  | Variable | [Discuss] |
| Law enforcement     | Variable | [Discuss] |

**Implication:** Any observed difference could be due to these factors rather than time of day per se.

### 8.3 Data Quality Limitations

1. **Reporting bias**
   - Data based on police reports, which may be more/less complete at different times
   - Minor crashes may be underreported

2. **Missing data**
   - We excluded crashes with missing values, which could bias results if missingness is related to severity or time

3. **Measurement precision**
   - Casualty counts may not fully capture crash severity
   - Does not account for injury severity levels
   - Does not include property damage

### 8.4 Generalizability

1. **Geographic specificity**
   - Results apply to NYC, which has unique characteristics (density, public transit, traffic patterns)
   - May not generalize to suburban or rural areas, or other cities

2. **Temporal specificity**
   - Data from [date range]
   - Traffic patterns and enforcement may have changed since then

### 8.5 Statistical Limitations

1. **Multiple comparisons**
   - If we conducted exploratory analyses (e.g., by hour), familywise error rate increases
   - Main hypothesis test (night vs day) is pre-specified

2. **Assumptions**
   - While t-test is robust with large n, data may still violate distributional assumptions
   - [Discuss any assumption violations and their potential impact]

---

## 9. Conclusion and Recommendations

### 9.1 Summary of Findings

This study investigated whether motor vehicle crashes occurring at night are more severe than those occurring during the day in New York City. Using [N] crashes, we compared mean casualties per crash between Night (18:00-05:59, n = [XXX]) and Day (06:00-17:59, n = [XXX]) groups.

**Key findings:**
- **[Finding 1]:** [State main statistical result]
- **[Finding 2]:** [State effect size and practical significance]
- **[Finding 3]:** [State any secondary findings]

**Answer to research question:**
[Clearly state whether nighttime crashes are more severe, and to what degree]

### 9.2 Implications

**For Traffic Safety Policy:**
- [Discuss how findings could inform interventions]
- [Suggest specific policies or programs]

**For Law Enforcement:**
- [Discuss patrol allocation]
- [Discuss DUI checkpoints or other enforcement strategies]

**For Public Awareness:**
- [Discuss education campaigns]
- [Discuss messaging to drivers]

**For Future Research:**
- [Suggest follow-up studies]
- [Identify variables to control or investigate further]

### 9.3 Recommendations

Based on our findings, we recommend:

1. **[Recommendation 1]**
   - [Explain rationale]
   
2. **[Recommendation 2]**
   - [Explain rationale]
   
3. **[Recommendation 3]**
   - [Explain rationale]

### 9.4 Future Directions

To build on this work, future research could:
- Control for confounding variables (e.g., weather, alcohol involvement)
- Analyze crash severity using more detailed injury classifications
- Compare night vs day patterns across different boroughs or neighborhoods
- Investigate interaction effects (e.g., night × weekend)
- Examine trends over time (has the gap changed?)
- Replicate in other cities

---

## 10. References

**Data Source:**
- NYC Open Data. (2024). Motor Vehicle Collisions - Crashes. https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

**Statistical Methods:**
- Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.
- Welch, B. L. (1947). The generalization of "Student's" problem when several different population variances are involved. *Biometrika*, 34(1-2), 28-35.

**Software:**
- Python Software Foundation. (2024). Python (Version 3.x). https://www.python.org/
- McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61.
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*, 92-96.

**[Add any other references you consulted]**

---

## Appendices

### Appendix A: Code Repository

All analysis code is available at: [GitHub repository URL]

- `data_clean.py`: Data cleaning pipeline
- `analysis.py`: Descriptive statistics and data processing
- `statistical_tests.py`: Hypothesis testing and power analysis
- `visualizations.py`: Figure generation
- `run_analysis.py`: Main analysis orchestration script

### Appendix B: Additional Figures

**[Include any supplementary figures not shown in main text]**

### Appendix C: Detailed Statistical Output

**[Optionally include full printout from statistical tests]**

---

**Word Count:** [Approximately 3000-4000 words]

**Figures:**
1. Distribution comparison (histograms, box plots, violin plots, CDF)
2. Q-Q plots for normality assessment
3. Statistical results visualization (mean comparison, effect size)
4. Hourly pattern analysis

**Tables:**
1. Descriptive statistics by group
2. Statistical test results
3. [Others as needed]

---

**Prepared by:** [Your Name] and [Partner Name]  
**Date:** November 4, 2024  
**Course:** [Course Name and Number]

