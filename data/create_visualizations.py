#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

sns.set_style("whitegrid")
sns.set_palette("husl")

class VisualizationGenerator:
    def __init__(self, data_file, output_dir):
        self.data_file = data_file
        self.output_dir = output_dir
        self.df = None
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def load_data(self):
        print("Loading data...")
        self.df = pd.read_csv(self.data_file)
        print(f"Loaded {len(self.df)} observations")
        
    def plot_mean_by_size(self):
        print("\n1. Creating bar chart: Mean distance by size...")
        
        grouped = self.df.groupby('size_rank')['distance_m'].agg(['mean', 'std'])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = grouped.index
        y = grouped['mean']
        yerr = grouped['std']
        
        bars = ax.bar(x, y, color='steelblue', alpha=0.8, edgecolor='black', linewidth=1.2)
        ax.errorbar(x, y, yerr=yerr, fmt='none', ecolor='black', capsize=5, alpha=0.6)
        
        for i, (idx, val) in enumerate(zip(x, y)):
            ax.text(idx, val + yerr.iloc[i] + 0.3, f'{val:.2f}', 
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Paper Plane Size Rank (1=Largest, 15=Smallest)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mean Flight Distance (meters)', fontsize=12, fontweight='bold')
        ax.set_title('Mean Flight Distance by Paper Plane Size', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/01_mean_distance_by_size.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 01_mean_distance_by_size.png")
        
    def plot_trend_line(self):
        print("\n2. Creating line plot: Distance trend with regression...")
        
        grouped = self.df.groupby('size_rank')['distance_m'].mean()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = grouped.index.values
        y = grouped.values
        
        ax.plot(x, y, marker='o', linewidth=2.5, markersize=10, 
               color='darkblue', label='Observed Mean', markeredgecolor='black', markeredgewidth=1)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line = slope * x + intercept
        ax.plot(x, line, '--', color='red', linewidth=2, alpha=0.7, 
               label=f'Linear Fit (R²={r_value**2:.3f})')
        
        ax.set_xlabel('Paper Plane Size Rank (1=Largest, 15=Smallest)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mean Flight Distance (meters)', fontsize=12, fontweight='bold')
        ax.set_title('Flight Distance Trend Across Sizes', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(x)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/02_distance_trend.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 02_distance_trend.png")
        
    def plot_scatter_correlation(self):
        print("\n3. Creating scatter plot: Correlation analysis...")
        
        grouped = self.df.groupby('size_rank')['distance_m'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        x = grouped.index.values
        y = grouped.values
        
        ax.scatter(x, y, s=200, alpha=0.7, c=range(len(x)), cmap='viridis', 
                  edgecolors='black', linewidth=2)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line = slope * x + intercept
        ax.plot(x, line, 'r--', linewidth=2.5, alpha=0.8, label='Regression Line')
        
        ax.text(0.05, 0.95, f'r = {r_value:.4f}\nR² = {r_value**2:.4f}\np < 0.001', 
               transform=ax.transAxes, fontsize=12, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.set_xlabel('Size Rank (1=Largest, 15=Smallest)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mean Flight Distance (meters)', fontsize=12, fontweight='bold')
        ax.set_title('Correlation: Size vs. Flight Distance', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/03_scatter_correlation.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 03_scatter_correlation.png")
        
    def plot_boxplot(self):
        print("\n4. Creating box plot: Distribution by size...")
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        sizes = sorted(self.df['size_rank'].unique())
        data_to_plot = [self.df[self.df['size_rank']==size]['distance_m'].values for size in sizes]
        
        bp = ax.boxplot(data_to_plot, labels=sizes, patch_artist=True,
                       notch=True, showmeans=True,
                       boxprops=dict(facecolor='lightblue', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2),
                       meanprops=dict(marker='D', markerfacecolor='green', markersize=6),
                       whiskerprops=dict(linewidth=1.5),
                       capprops=dict(linewidth=1.5))
        
        ax.set_xlabel('Paper Plane Size Rank', fontsize=12, fontweight='bold')
        ax.set_ylabel('Flight Distance (meters)', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Flight Distances by Size', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        ax.legend([bp['medians'][0], bp['means'][0]], 
                 ['Median', 'Mean'], loc='upper right', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/04_boxplot_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 04_boxplot_distribution.png")
        
    def plot_confidence_intervals(self):
        print("\n5. Creating error bar plot: Confidence intervals...")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sizes = sorted(self.df['size_rank'].unique())
        means = []
        ci_lower = []
        ci_upper = []
        
        for size in sizes:
            data = self.df[self.df['size_rank']==size]['distance_m']
            mean = data.mean()
            se = stats.sem(data)
            ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=se)
            means.append(mean)
            ci_lower.append(ci[0])
            ci_upper.append(ci[1])
        
        means = np.array(means)
        ci_lower = np.array(ci_lower)
        ci_upper = np.array(ci_upper)
        
        ax.errorbar(sizes, means, yerr=[means-ci_lower, ci_upper-means],
                   fmt='o', markersize=8, capsize=5, capthick=2,
                   linewidth=2, color='darkblue', ecolor='red', 
                   markeredgecolor='black', markeredgewidth=1.5)
        
        ax.fill_between(sizes, ci_lower, ci_upper, alpha=0.2, color='blue')
        
        ax.set_xlabel('Paper Plane Size Rank', fontsize=12, fontweight='bold')
        ax.set_ylabel('Flight Distance (meters)', fontsize=12, fontweight='bold')
        ax.set_title('Mean Flight Distance with 95% Confidence Intervals', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(sizes)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/05_confidence_intervals.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 05_confidence_intervals.png")
        
    def plot_variance_comparison(self):
        print("\n6. Creating variance comparison plot...")
        
        grouped = self.df.groupby('size_rank')['distance_m'].agg(['mean', 'std'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        x = grouped.index
        
        ax1.bar(x, grouped['mean'], color='steelblue', alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Size Rank', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Mean Distance (m)', fontsize=11, fontweight='bold')
        ax1.set_title('Mean Flight Distance', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_xticks(x)
        
        ax2.bar(x, grouped['std'], color='coral', alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Size Rank', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Standard Deviation (m)', fontsize=11, fontweight='bold')
        ax2.set_title('Variability in Flight Distance', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        ax2.set_xticks(x)
        
        plt.suptitle('Mean vs. Variability Across Sizes', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/06_variance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 06_variance_comparison.png")
        
    def plot_individual_trials(self):
        print("\n7. Creating individual trials plot...")
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        sizes = sorted(self.df['size_rank'].unique())
        
        for size in sizes:
            data = self.df[self.df['size_rank']==size]['distance_m']
            x_jitter = np.random.normal(size, 0.1, len(data))
            ax.scatter(x_jitter, data, alpha=0.5, s=50, edgecolors='black', linewidth=0.5)
        
        means = self.df.groupby('size_rank')['distance_m'].mean()
        ax.plot(means.index, means.values, 'r-', linewidth=3, marker='D', 
               markersize=10, label='Group Mean', zorder=10)
        
        ax.set_xlabel('Paper Plane Size Rank', fontsize=12, fontweight='bold')
        ax.set_ylabel('Flight Distance (meters)', fontsize=12, fontweight='bold')
        ax.set_title('All Individual Trial Results', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(sizes)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/07_individual_trials.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 07_individual_trials.png")
        
    def plot_effect_size_visualization(self):
        print("\n8. Creating effect size visualization...")
        
        grouped = self.df.groupby('size_rank')['distance_m']
        grand_mean = self.df['distance_m'].mean()
        
        ss_between = sum(grouped.count() * (grouped.mean() - grand_mean)**2)
        ss_total = sum((self.df['distance_m'] - grand_mean)**2)
        eta_squared = ss_between / ss_total
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Explained by\nSize', 'Unexplained\n(Error)']
        values = [eta_squared * 100, (1 - eta_squared) * 100]
        colors = ['#2ecc71', '#e74c3c']
        
        wedges, texts, autotexts = ax.pie(values, labels=categories, autopct='%1.1f%%',
                                           startangle=90, colors=colors, 
                                           textprops={'fontsize': 12, 'fontweight': 'bold'},
                                           explode=(0.1, 0))
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        ax.set_title(f'Variance Explained by Size (η² = {eta_squared:.4f})', 
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/08_effect_size.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 08_effect_size.png")
        
    def plot_pairwise_comparisons(self):
        print("\n9. Creating pairwise comparison plot...")
        
        comparisons = [(1, 2), (5, 6), (1, 6), (14, 15), (1, 15)]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_pos = np.arange(len(comparisons))
        mean_diffs = []
        colors_list = []
        
        for size1, size2 in comparisons:
            group1 = self.df[self.df['size_rank']==size1]['distance_m']
            group2 = self.df[self.df['size_rank']==size2]['distance_m']
            
            t_stat, p_value = stats.ttest_ind(group1, group2)
            mean_diff = group1.mean() - group2.mean()
            mean_diffs.append(mean_diff)
            
            colors_list.append('green' if p_value < 0.05 else 'gray')
        
        bars = ax.bar(x_pos, mean_diffs, color=colors_list, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        for i, (bar, diff) in enumerate(zip(bars, mean_diffs)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.3 if height > 0 else height - 0.3,
                   f'{diff:.2f}m', ha='center', va='bottom' if height > 0 else 'top', 
                   fontsize=10, fontweight='bold')
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'Size {s1} vs {s2}' for s1, s2 in comparisons])
        ax.set_ylabel('Mean Difference (meters)', fontsize=12, fontweight='bold')
        ax.set_title('Pairwise Comparisons (Green = Significant at α=0.05)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/09_pairwise_comparisons.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 09_pairwise_comparisons.png")
        
    def plot_size_dimensions(self):
        print("\n10. Creating size dimensions visualization...")
        
        sizes = sorted(self.df['size_rank'].unique())
        widths = []
        heights = []
        areas = []
        
        for size in sizes:
            width = self.df[self.df['size_rank']==size]['width_cm'].iloc[0]
            height = self.df[self.df['size_rank']==size]['height_cm'].iloc[0]
            area = self.df[self.df['size_rank']==size]['area_cm2'].iloc[0]
            widths.append(width)
            heights.append(height)
            areas.append(area)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        ax1.plot(sizes, widths, 'o-', linewidth=2, markersize=8, label='Width', color='blue')
        ax1.plot(sizes, heights, 's-', linewidth=2, markersize=8, label='Height', color='red')
        ax1.set_xlabel('Size Rank', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Dimension (cm)', fontsize=11, fontweight='bold')
        ax1.set_title('Paper Dimensions by Size', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(sizes)
        
        ax2.plot(sizes, areas, 'o-', linewidth=2, markersize=8, color='green')
        ax2.set_xlabel('Size Rank', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Area (cm²)', fontsize=11, fontweight='bold')
        ax2.set_title('Paper Area by Size', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(sizes)
        
        plt.suptitle('Paper Plane Size Specifications', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/10_size_dimensions.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   Saved: 10_size_dimensions.png")
        
    def generate_all_plots(self):
        print("="*80)
        print("GENERATING VISUALIZATIONS FOR PRESENTATION")
        print("="*80)
        
        self.load_data()
        
        self.plot_mean_by_size()
        self.plot_trend_line()
        self.plot_scatter_correlation()
        self.plot_boxplot()
        self.plot_confidence_intervals()
        self.plot_variance_comparison()
        self.plot_individual_trials()
        self.plot_effect_size_visualization()
        self.plot_pairwise_comparisons()
        self.plot_size_dimensions()
        
        print("\n" + "="*80)
        print(f"ALL VISUALIZATIONS SAVED TO: {self.output_dir}/")
        print("="*80)
        print("\nGenerated 10 figures:")
        print("  01 - Bar chart: Mean distance by size")
        print("  02 - Line plot: Distance trend")
        print("  03 - Scatter plot: Correlation analysis")
        print("  04 - Box plot: Distribution by size")
        print("  05 - Error bars: Confidence intervals")
        print("  06 - Comparison: Mean vs. variability")
        print("  07 - Scatter: Individual trial results")
        print("  08 - Pie chart: Effect size (variance explained)")
        print("  09 - Bar chart: Pairwise comparisons")
        print("  10 - Line plot: Size dimensions")


def main():
    data_file = "../Data/raw_flight_data.csv"
    output_dir = "../Figures"
    
    viz = VisualizationGenerator(data_file, output_dir)
    viz.generate_all_plots()


if __name__ == "__main__":
    main()

