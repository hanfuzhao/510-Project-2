

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10


class CrashVisualizer:
    
    def __init__(self, df, night_data, day_data, output_dir="/Users/leo/Desktop/510 Project 2/figures"):
        self.df = df
        self.night_data = np.array(night_data)
        self.day_data = np.array(day_data)
        self.output_dir = output_dir
        
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_distributions(self):
        max_plot_size = 100000
        night_plot = self.night_data if len(self.night_data) <= max_plot_size else \
                     np.random.choice(self.night_data, size=max_plot_size, replace=False)
        day_plot = self.day_data if len(self.day_data) <= max_plot_size else \
                   np.random.choice(self.day_data, size=max_plot_size, replace=False)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        ax1 = axes[0, 0]
        ax1.hist(night_plot, bins=50, alpha=0.6, label='Night', 
                 color='navy', density=True, edgecolor='black')
        ax1.hist(day_plot, bins=50, alpha=0.6, label='Day', 
                 color='orange', density=True, edgecolor='black')
        ax1.set_xlabel('Total Casualties per Crash')
        ax1.set_ylabel('Density')
        ax1.set_title('Distribution of Crash Severity: Night vs Day')
        ax1.legend()
        ax1.set_xlim(0, min(20, max(night_plot.max(), day_plot.max())))
        
        ax2 = axes[0, 1]
        box_data = [night_plot, day_plot]
        bp = ax2.boxplot(box_data, labels=['Night\n(18:00-05:59)', 'Day\n(06:00-17:59)'],
                         patch_artist=True, notch=True, showmeans=True)
        bp['boxes'][0].set_facecolor('navy')
        bp['boxes'][1].set_facecolor('orange')
        for patch in bp['boxes']:
            patch.set_alpha(0.6)
        ax2.set_ylabel('Total Casualties per Crash')
        ax2.set_title('Box Plot Comparison')
        ax2.grid(axis='y', alpha=0.3)
        
        ax3 = axes[1, 0]
        plot_df = pd.DataFrame({
            'Casualties': np.concatenate([night_plot, day_plot]),
            'Time Period': ['Night'] * len(night_plot) + ['Day'] * len(day_plot)
        })
        sns.violinplot(data=plot_df, x='Time Period', y='Casualties', 
                      palette={'Night': 'navy', 'Day': 'orange'}, ax=ax3)
        ax3.set_ylabel('Total Casualties per Crash')
        ax3.set_title('Violin Plot Comparison')
        ax3.set_ylim(0, min(20, plot_df['Casualties'].max()))
        
        ax4 = axes[1, 1]
        percentiles = np.linspace(0, 100, 1000)
        night_percentile_vals = np.percentile(self.night_data, percentiles)
        day_percentile_vals = np.percentile(self.day_data, percentiles)
        ax4.plot(night_percentile_vals, percentiles/100, label='Night', color='navy', linewidth=2)
        ax4.plot(day_percentile_vals, percentiles/100, label='Day', color='orange', linewidth=2)
        ax4.set_xlabel('Total Casualties per Crash')
        ax4.set_ylabel('Cumulative Probability')
        ax4.set_title('Cumulative Distribution Function')
        ax4.legend()
        ax4.grid(alpha=0.3)
        ax4.set_xlim(0, min(20, max(self.night_data.max(), self.day_data.max())))
        
        plt.tight_layout()
        save_path = f"{self.output_dir}/distribution_comparison.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
        plt.close()
    
    def plot_hourly_patterns(self):
        hourly_stats = self.df.groupby('crash_hour').agg({
            'total_casualties': ['count', 'sum', 'mean', 'std']
        }).reset_index()
        
        hourly_stats.columns = ['Hour', 'Count', 'Total', 'Mean', 'Std']
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        colors = ['navy' if (h >= 18 or h < 6) else 'orange' for h in hourly_stats['Hour']]
        
        ax1 = axes[0]
        bars1 = ax1.bar(hourly_stats['Hour'], hourly_stats['Mean'], 
                        color=colors, alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Mean Casualties per Crash')
        ax1.set_title('Average Crash Severity by Hour of Day')
        ax1.set_xticks(range(0, 24))
        ax1.grid(axis='y', alpha=0.3)
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='navy', alpha=0.7, label='Night (18:00-05:59)'),
            Patch(facecolor='orange', alpha=0.7, label='Day (06:00-17:59)')
        ]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        ax2 = axes[1]
        bars2 = ax2.bar(hourly_stats['Hour'], hourly_stats['Count'], 
                        color=colors, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Hour of Day')
        ax2.set_ylabel('Number of Crashes')
        ax2.set_title('Crash Frequency by Hour of Day')
        ax2.set_xticks(range(0, 24))
        ax2.grid(axis='y', alpha=0.3)
        ax2.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        save_path = f"{self.output_dir}/hourly_patterns.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
        plt.close()
    
    def plot_statistical_results(self, test_results):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1 = axes[0]
        means = [test_results['mean_night'], test_results['mean_day']]
        labels = ['Night\n(18:00-05:59)', 'Day\n(06:00-17:59)']
        
        se_night = stats.sem(self.night_data)
        se_day = stats.sem(self.day_data)
        errors = [se_night * 1.96, se_day * 1.96]
        
        bars = ax1.bar(labels, means, color=['navy', 'orange'], 
                      alpha=0.7, edgecolor='black', width=0.6)
        ax1.errorbar(labels, means, yerr=errors, fmt='none', 
                    color='black', capsize=10, capthick=2, linewidth=2)
        ax1.set_ylabel('Mean Casualties per Crash')
        ax1.set_title('Mean Comparison with 95% CI')
        ax1.grid(axis='y', alpha=0.3)
        
        for i, (mean, err) in enumerate(zip(means, errors)):
            ax1.text(i, mean + err + 0.01, f'{mean:.3f}', 
                    ha='center', va='bottom', fontweight='bold')
        
        ax2 = axes[1]
        cohens_d = test_results['cohens_d']
        
        ax2.barh(['Effect Size'], [abs(cohens_d)], color='steelblue', alpha=0.7)
        ax2.axvline(0.2, color='green', linestyle='--', linewidth=2, label='Small (0.2)')
        ax2.axvline(0.5, color='orange', linestyle='--', linewidth=2, label='Medium (0.5)')
        ax2.axvline(0.8, color='red', linestyle='--', linewidth=2, label='Large (0.8)')
        ax2.set_xlabel("Cohen's d")
        ax2.set_title(f"Effect Size: d = {cohens_d:.4f}\n({test_results['effect_interpretation']})")
        ax2.legend(loc='lower right')
        ax2.set_xlim(0, max(1.0, abs(cohens_d) + 0.1))
        
        plt.tight_layout()
        save_path = f"{self.output_dir}/statistical_results.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
        plt.close()
    
    def plot_qq_plots(self):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        sample_size = min(5000, len(self.night_data), len(self.day_data))
        night_sample = np.random.choice(self.night_data, size=sample_size, replace=False)
        day_sample = np.random.choice(self.day_data, size=sample_size, replace=False)
        
        stats.probplot(night_sample, dist="norm", plot=axes[0])
        axes[0].set_title('Q-Q Plot: Night Crashes')
        axes[0].grid(alpha=0.3)
        
        stats.probplot(day_sample, dist="norm", plot=axes[1])
        axes[1].set_title('Q-Q Plot: Day Crashes')
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        save_path = f"{self.output_dir}/qq_plots.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
        plt.close()
    
    def create_all_visualizations(self, test_results=None):
        print("\n" + "="*70)
        print("CREATING VISUALIZATIONS")
        print("="*70 + "\n")
        
        self.plot_distributions()
        self.plot_hourly_patterns()
        self.plot_qq_plots()
        
        if test_results:
            self.plot_statistical_results(test_results)
        
        print(f"\nAll figures saved to: {self.output_dir}/")


if __name__ == "__main__":
    print("This module should be imported and used with real data.")
    print("See run_analysis.py for complete workflow.")

