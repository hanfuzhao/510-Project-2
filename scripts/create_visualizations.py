

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 10

print("Loading data (columns only)...")
df = pd.read_csv("/Users/leo/Desktop/510 Project 2/data/cleaned_final.csv", 
                 usecols=['crash_time', 'number_of_persons_injured', 
                         'number_of_persons_killed'])

df['crash_hour'] = pd.to_datetime(df['crash_time'], format='%H:%M', errors='coerce').dt.hour
df['total_casualties'] = df['number_of_persons_injured'] + df['number_of_persons_killed']
df['time_period'] = df['crash_hour'].apply(lambda h: 'Night' if (h >= 18 or h < 6) else 'Day')

night_data = df[df['time_period'] == 'Night']['total_casualties'].values
day_data = df[df['time_period'] == 'Day']['total_casualties'].values

os.makedirs("/Users/leo/Desktop/510 Project 2/figures", exist_ok=True)

print(f"Night: {len(night_data):,}, Day: {len(day_data):,}")

print("\nCreating Figure 1: Box plot comparison...")

np.random.seed(42)
night_sample = np.random.choice(night_data, size=min(50000, len(night_data)), replace=False)
day_sample = np.random.choice(day_data, size=min(50000, len(day_data)), replace=False)

fig, ax = plt.subplots(figsize=(8, 6))
bp = ax.boxplot([night_sample, day_sample], 
                labels=['Night\n(18:00-05:59)', 'Day\n(06:00-17:59)'],
                patch_artist=True, notch=True, showmeans=True)
bp['boxes'][0].set_facecolor('navy')
bp['boxes'][1].set_facecolor('orange')
for patch in bp['boxes']:
    patch.set_alpha(0.6)

ax.set_ylabel('Total Casualties per Crash', fontsize=12)
ax.set_title('Crash Severity Comparison: Night vs Day', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/leo/Desktop/510 Project 2/figures/boxplot_comparison.png', dpi=150)
print("✓ Saved: figures/boxplot_comparison.png")
plt.close()

print("Creating Figure 2: Mean comparison...")

mean_night = night_data.mean()
mean_day = day_data.mean()
se_night = stats.sem(night_data)
se_day = stats.sem(day_data)
ci_night = 1.96 * se_night
ci_day = 1.96 * se_day

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(['Night\n(18:00-05:59)', 'Day\n(06:00-17:59)'], 
              [mean_night, mean_day],
              color=['navy', 'orange'], alpha=0.7, edgecolor='black', width=0.5)
ax.errorbar(['Night\n(18:00-05:59)', 'Day\n(06:00-17:59)'], 
           [mean_night, mean_day],
           yerr=[ci_night, ci_day],
           fmt='none', color='black', capsize=15, capthick=2, linewidth=2)

ax.text(0, mean_night + ci_night + 0.01, f'{mean_night:.4f}', 
       ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.text(1, mean_day + ci_day + 0.01, f'{mean_day:.4f}', 
       ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_ylabel('Mean Casualties per Crash', fontsize=12)
ax.set_title('Mean Casualties with 95% Confidence Intervals', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/leo/Desktop/510 Project 2/figures/mean_comparison.png', dpi=150)
print("✓ Saved: figures/mean_comparison.png")
plt.close()

print("Creating Figure 3: Hourly patterns...")

hourly_stats = df.groupby('crash_hour').agg({
    'total_casualties': ['count', 'mean']
}).reset_index()
hourly_stats.columns = ['Hour', 'Count', 'Mean']

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

colors = ['navy' if (h >= 18 or h < 6) else 'orange' for h in hourly_stats['Hour']]

ax1.bar(hourly_stats['Hour'], hourly_stats['Mean'], color=colors, alpha=0.7, edgecolor='black')
ax1.set_xlabel('Hour of Day', fontsize=11)
ax1.set_ylabel('Mean Casualties per Crash', fontsize=11)
ax1.set_title('Average Crash Severity by Hour of Day', fontsize=13, fontweight='bold')
ax1.set_xticks(range(0, 24))
ax1.grid(axis='y', alpha=0.3)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='navy', alpha=0.7, label='Night (18:00-05:59)'),
    Patch(facecolor='orange', alpha=0.7, label='Day (06:00-17:59)')
]
ax1.legend(handles=legend_elements, loc='upper right')

ax2.bar(hourly_stats['Hour'], hourly_stats['Count'], color=colors, alpha=0.7, edgecolor='black')
ax2.set_xlabel('Hour of Day', fontsize=11)
ax2.set_ylabel('Number of Crashes', fontsize=11)
ax2.set_title('Crash Frequency by Hour of Day', fontsize=13, fontweight='bold')
ax2.set_xticks(range(0, 24))
ax2.grid(axis='y', alpha=0.3)
ax2.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig('/Users/leo/Desktop/510 Project 2/figures/hourly_patterns.png', dpi=150)
print("✓ Saved: figures/hourly_patterns.png")
plt.close()

print("Creating Figure 4: Distribution comparison...")

fig, ax = plt.subplots(figsize=(10, 6))

night_hist = night_sample[night_sample <= 10]
day_hist = day_sample[day_sample <= 10]

ax.hist(night_hist, bins=11, alpha=0.6, label=f'Night (n={len(night_data):,})', 
        color='navy', edgecolor='black', density=True)
ax.hist(day_hist, bins=11, alpha=0.6, label=f'Day (n={len(day_data):,})', 
        color='orange', edgecolor='black', density=True)

ax.set_xlabel('Total Casualties per Crash', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Distribution of Crash Severity (0-10 casualties)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/leo/Desktop/510 Project 2/figures/distribution_histogram.png', dpi=150)
print("✓ Saved: figures/distribution_histogram.png")
plt.close()

print("Creating Figure 5: Effect size...")

cohens_d = 0.1245

fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(['Observed\nEffect Size'], [abs(cohens_d)], color='steelblue', alpha=0.7, height=0.3)

ax.axvline(0.2, color='green', linestyle='--', linewidth=2, label='Small (0.2)', alpha=0.7)
ax.axvline(0.5, color='orange', linestyle='--', linewidth=2, label='Medium (0.5)', alpha=0.7)
ax.axvline(0.8, color='red', linestyle='--', linewidth=2, label='Large (0.8)', alpha=0.7)

ax.set_xlabel("Cohen's d", fontsize=12)
ax.set_title(f"Effect Size: d = {cohens_d:.4f} (Negligible to Small)", 
            fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.set_xlim(0, 1.0)
ax.grid(axis='x', alpha=0.3)

ax.text(cohens_d, 0, f'  {cohens_d:.4f}', va='center', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('/Users/leo/Desktop/510 Project 2/figures/effect_size.png', dpi=150)
print("✓ Saved: figures/effect_size.png")
plt.close()

print("Creating Figure 6: Proportion with casualties...")

night_with = (night_data > 0).sum()
day_with = (day_data > 0).sum()
night_pct = 100 * night_with / len(night_data)
day_pct = 100 * day_with / len(day_data)

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(['Night', 'Day'], [night_pct, day_pct], 
             color=['navy', 'orange'], alpha=0.7, edgecolor='black', width=0.5)

ax.text(0, night_pct + 0.5, f'{night_pct:.2f}%\n({night_with:,} crashes)', 
       ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.text(1, day_pct + 0.5, f'{day_pct:.2f}%\n({day_with:,} crashes)', 
       ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.set_ylabel('Percentage of Crashes', fontsize=12)
ax.set_title('Proportion of Crashes with Casualties (Injured or Killed > 0)', 
            fontsize=13, fontweight='bold')
ax.set_ylim(0, max(night_pct, day_pct) + 5)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/leo/Desktop/510 Project 2/figures/casualties_proportion.png', dpi=150)
print("✓ Saved: figures/casualties_proportion.png")
plt.close()

print("\n" + "="*80)
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY")
print("="*80)
print("\nGenerated figures:")
print("  1. boxplot_comparison.png - Box plots showing distribution")
print("  2. mean_comparison.png - Mean values with 95% CI")
print("  3. hourly_patterns.png - Hourly trends")
print("  4. distribution_histogram.png - Distribution comparison")
print("  5. effect_size.png - Cohen's d visualization")
print("  6. casualties_proportion.png - Percentage with casualties")
print(f"\nAll saved in: /Users/leo/Desktop/510 Project 2/figures/")

