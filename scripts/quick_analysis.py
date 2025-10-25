

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower
from datetime import datetime

print("="*80)
print("NYC MOTOR VEHICLE CRASH SEVERITY ANALYSIS (QUICK VERSION)".center(80))
print("="*80)
print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print("Loading data...")
data_path = "/Users/leo/Desktop/510 Project 2/data/cleaned_final.csv"

df = pd.read_csv(data_path, usecols=[
    'crash_time', 'crash_date',
    'number_of_persons_injured', 'number_of_persons_killed'
])

print(f"Loaded {len(df):,} records")

print("\nClassifying time periods...")
df['crash_hour'] = pd.to_datetime(df['crash_time'], format='%H:%M', errors='coerce').dt.hour
df['total_casualties'] = df['number_of_persons_injured'] + df['number_of_persons_killed']
df['time_period'] = df['crash_hour'].apply(lambda h: 'Night' if (h >= 18 or h < 6) else 'Day')

night_data = df[df['time_period'] == 'Night']['total_casualties'].values
day_data = df[df['time_period'] == 'Day']['total_casualties'].values

print(f"Night crashes (18:00-05:59): {len(night_data):,}")
print(f"Day crashes (06:00-17:59): {len(day_data):,}")

print("\n" + "="*80)
print("DESCRIPTIVE STATISTICS")
print("="*80)

stats_data = {
    'Group': ['Night', 'Day'],
    'N': [len(night_data), len(day_data)],
    'Mean': [night_data.mean(), day_data.mean()],
    'Std': [night_data.std(), day_data.std()],
    'Median': [np.median(night_data), np.median(day_data)],
    'Q1': [np.percentile(night_data, 25), np.percentile(day_data, 25)],
    'Q3': [np.percentile(night_data, 75), np.percentile(day_data, 75)],
    'Min': [night_data.min(), day_data.min()],
    'Max': [night_data.max(), day_data.max()]
}

stats_df = pd.DataFrame(stats_data)
print(stats_df.to_string(index=False))

mean_diff = night_data.mean() - day_data.mean()
print(f"\nMean Difference (Night - Day): {mean_diff:.4f}")

night_with = (night_data > 0).sum()
day_with = (day_data > 0).sum()
print(f"\nCrashes with casualties:")
print(f"  Night: {night_with:,} ({100*night_with/len(night_data):.2f}%)")
print(f"  Day: {day_with:,} ({100*day_with/len(day_data):.2f}%)")

print("\n" + "="*80)
print("ASSUMPTION CHECKS")
print("="*80)

print("\n1. Homogeneity of Variance (Levene's test):")
levene_stat, levene_p = stats.levene(night_data, day_data)
print(f"   Statistic={levene_stat:.4f}, p={levene_p:.6f}")

if levene_p < 0.05:
    print("   → Variances differ significantly, use Welch's t-test")
    equal_var = False
else:
    print("   → Variances are approximately equal")
    equal_var = True

print("\n2. Normality:")
print("   With N > 400,000 in each group, Central Limit Theorem applies")
print("   t-test is robust to non-normality with large samples")

print("\n" + "="*80)
print("EFFECT SIZE")
print("="*80)

n1, n2 = len(night_data), len(day_data)
var1, var2 = night_data.var(ddof=1), day_data.var(ddof=1)
pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
cohens_d = mean_diff / pooled_std

if abs(cohens_d) < 0.2:
    effect_interpretation = "negligible"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "small"
elif abs(cohens_d) < 0.8:
    effect_interpretation = "medium"
else:
    effect_interpretation = "large"

print(f"\nCohen's d: {cohens_d:.4f}")
print(f"Interpretation: {effect_interpretation} effect")

print("\n" + "="*80)
print("POWER ANALYSIS")
print("="*80)

power_analyzer = TTestIndPower()
ratio = n2 / n1

print(f"\nUsing observed effect size: d = {cohens_d:.4f}")
print(f"Sample sizes: Night N={n1:,}, Day N={n2:,}")
print(f"Significance level: α = 0.05")

achieved_power = power_analyzer.solve_power(
    effect_size=abs(cohens_d),
    nobs1=n1,
    ratio=ratio,
    alpha=0.05,
    alternative='two-sided'
)

print(f"\nAchieved Power: {achieved_power:.4f} ({achieved_power*100:.2f}%)")

if achieved_power >= 0.8:
    print("✓ Power is adequate (≥ 0.80)")
else:
    print("✗ Power is below threshold (0.80)")

mde = power_analyzer.solve_power(
    effect_size=None,
    nobs1=n1,
    ratio=ratio,
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
)
print(f"\nMinimum Detectable Effect (80% power): d = {mde:.4f}")

print("\n" + "="*80)
print("INDEPENDENT SAMPLES T-TEST")
print("="*80)

t_stat, p_value = stats.ttest_ind(night_data, day_data, equal_var=equal_var)

se_night = stats.sem(night_data)
se_day = stats.sem(day_data)
se_diff = np.sqrt(se_night**2 + se_day**2)

if equal_var:
    df_val = n1 + n2 - 2
    test_type = "Standard Independent t-test"
else:
    s1, s2 = night_data.std(ddof=1), day_data.std(ddof=1)
    df_val = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
    test_type = "Welch's t-test"

ci_margin = stats.t.ppf(0.975, df_val) * se_diff
ci_lower = mean_diff - ci_margin
ci_upper = mean_diff + ci_margin

print(f"\nTest Type: {test_type}")
print(f"\nHypotheses:")
print(f"  H₀: μ_night = μ_day")
print(f"  H₁: μ_night ≠ μ_day")
print(f"\nResults:")
print(f"  Night mean: {night_data.mean():.4f} (SE = {se_night:.4f})")
print(f"  Day mean:   {day_data.mean():.4f} (SE = {se_day:.4f})")
print(f"  Mean difference: {mean_diff:.4f}")
print(f"\n  t-statistic: {t_stat:.4f}")
print(f"  Degrees of freedom: {df_val:.2f}")
print(f"  p-value: {p_value:.6f}")
print(f"\n  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"\n  Cohen's d: {cohens_d:.4f} ({effect_interpretation})")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80 + "\n")

if p_value < 0.05:
    print(f"✓ REJECT H₀ (p = {p_value:.6f} < 0.05)")
    print(f"\n  → Statistically significant difference detected")
    if mean_diff > 0:
        print(f"  → Night crashes have HIGHER average casualties than day crashes")
        print(f"  → Difference: {mean_diff:.4f} casualties per crash")
    else:
        print(f"  → Day crashes have HIGHER average casualties than night crashes")
        print(f"  → Difference: {abs(mean_diff):.4f} casualties per crash")
else:
    print(f"✗ FAIL TO REJECT H₀ (p = {p_value:.6f} ≥ 0.05)")
    print(f"\n  → No statistically significant difference detected")

print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80 + "\n")

output_file = "/Users/leo/Desktop/510 Project 2/results/analysis_results_quick.txt"

with open(output_file, 'w') as f:
    f.write("NYC MOTOR VEHICLE CRASH SEVERITY ANALYSIS\n")
    f.write("Night vs Day Comparison\n")
    f.write("="*80 + "\n\n")
    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("SAMPLE SIZES\n")
    f.write(f"Night: {len(night_data):,}\n")
    f.write(f"Day: {len(day_data):,}\n\n")
    
    f.write("DESCRIPTIVE STATISTICS\n")
    f.write(stats_df.to_string(index=False))
    f.write(f"\n\nMean Difference: {mean_diff:.4f}\n\n")
    
    f.write("STATISTICAL TEST\n")
    f.write(f"Test: {test_type}\n")
    f.write(f"t({df_val:.2f}) = {t_stat:.4f}, p = {p_value:.6f}\n")
    f.write(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]\n")
    f.write(f"Cohen's d: {cohens_d:.4f} ({effect_interpretation})\n\n")
    
    f.write("POWER ANALYSIS\n")
    f.write(f"Achieved power: {achieved_power:.4f}\n")
    f.write(f"MDE (80% power): {mde:.4f}\n\n")
    
    f.write("CONCLUSION\n")
    if p_value < 0.05:
        f.write("REJECT H₀ - Significant difference detected\n")
    else:
        f.write("FAIL TO REJECT H₀ - No significant difference\n")

print(f"Results saved to: {output_file}")

print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)

