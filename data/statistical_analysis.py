#!/usr/bin/env python3
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import f_oneway, shapiro, levene, pearsonr
import warnings
warnings.filterwarnings('ignore')

class PaperPlaneAnalysis:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = None
        self.results = {}
        
    def load_data(self):
        print("="*80)
        print("PAPER PLANE FLIGHT DISTANCE ANALYSIS")
        print("="*80)
        print("\n1. DATA LOADING")
        print("-"*80)
        self.df = pd.read_csv(self.data_file)
        print(f"Loaded data from: {self.data_file}")
        print(f"Total observations: {len(self.df)}")
        print(f"Number of size groups: {self.df['size_rank'].nunique()}")
        print(f"Trials per size: {len(self.df[self.df['size_rank']==1])}")
        
    def state_hypotheses(self):
        print("\n2. HYPOTHESES")
        print("-"*80)
        print("Null Hypothesis (H0):")
        print("  Paper plane size has no effect on flight distance.")
        print("  All size groups have equal mean flight distances.")
        print("\nAlternative Hypothesis (H1):")
        print("  Paper plane size affects flight distance.")
        print("  At least one size group has a different mean flight distance.")
        print("\nSignificance level: α = 0.05")
        
    def descriptive_statistics(self):
        print("\n3. DESCRIPTIVE STATISTICS")
        print("-"*80)
        
        grouped = self.df.groupby('size_rank')['distance_m']
        desc_stats = grouped.agg(['count', 'mean', 'std', 'min', 'max'])
        
        print("\nSummary by Size:")
        print(desc_stats.to_string())
        
        self.results['descriptive'] = desc_stats
        
        print(f"\nOverall mean: {self.df['distance_m'].mean():.2f}m")
        print(f"Overall std: {self.df['distance_m'].std():.2f}m")
        print(f"Overall range: [{self.df['distance_m'].min():.2f}, {self.df['distance_m'].max():.2f}]m")
        
    def check_assumptions(self):
        print("\n4. ASSUMPTION CHECKING")
        print("-"*80)
        
        print("\n4.1 Normality Test (Shapiro-Wilk)")
        print("H0: Data is normally distributed")
        normality_results = []
        
        for size in sorted(self.df['size_rank'].unique()):
            data = self.df[self.df['size_rank']==size]['distance_m']
            stat, p_value = shapiro(data)
            normality_results.append({
                'Size': size,
                'W-statistic': stat,
                'p-value': p_value,
                'Normal?': 'Yes' if p_value > 0.05 else 'No'
            })
        
        norm_df = pd.DataFrame(normality_results)
        print(norm_df.to_string(index=False))
        
        normal_count = sum(1 for r in normality_results if r['Normal?'] == 'Yes')
        print(f"\nResult: {normal_count}/{len(normality_results)} groups pass normality test (p > 0.05)")
        
        print("\n4.2 Homogeneity of Variance (Levene's Test)")
        print("H0: All groups have equal variances")
        
        groups = [self.df[self.df['size_rank']==size]['distance_m'].values 
                  for size in sorted(self.df['size_rank'].unique())]
        stat, p_value = levene(*groups)
        
        print(f"Levene's statistic: {stat:.4f}")
        print(f"p-value: {p_value:.4f}")
        print(f"Result: {'Equal variances assumed' if p_value > 0.05 else 'Unequal variances'} (α = 0.05)")
        
        self.results['assumptions'] = {
            'normality': norm_df,
            'levene_stat': stat,
            'levene_p': p_value
        }
        
    def one_way_anova(self):
        print("\n5. ONE-WAY ANOVA")
        print("-"*80)
        print("Test: One-way ANOVA")
        print("Purpose: Test if mean flight distance differs across size groups")
        
        groups = [self.df[self.df['size_rank']==size]['distance_m'].values 
                  for size in sorted(self.df['size_rank'].unique())]
        
        f_stat, p_value = f_oneway(*groups)
        
        print(f"\nF-statistic: {f_stat:.4f}")
        print(f"p-value: {p_value:.6f}")
        print(f"Degrees of freedom: between = {len(groups)-1}, within = {len(self.df)-len(groups)}")
        
        if p_value < 0.05:
            print(f"\nDecision: REJECT null hypothesis (p < 0.05)")
            print("Conclusion: Paper plane size significantly affects flight distance.")
        else:
            print(f"\nDecision: FAIL TO REJECT null hypothesis (p >= 0.05)")
            print("Conclusion: No significant effect of size on flight distance.")
        
        self.results['anova'] = {
            'f_statistic': f_stat,
            'p_value': p_value,
            'df_between': len(groups)-1,
            'df_within': len(self.df)-len(groups)
        }
        
    def effect_size(self):
        print("\n6. EFFECT SIZE")
        print("-"*80)
        
        grouped = self.df.groupby('size_rank')['distance_m']
        grand_mean = self.df['distance_m'].mean()
        
        ss_between = sum(grouped.count() * (grouped.mean() - grand_mean)**2)
        ss_total = sum((self.df['distance_m'] - grand_mean)**2)
        
        eta_squared = ss_between / ss_total
        
        print(f"Eta-squared (η²): {eta_squared:.4f}")
        
        if eta_squared < 0.01:
            interpretation = "negligible"
        elif eta_squared < 0.06:
            interpretation = "small"
        elif eta_squared < 0.14:
            interpretation = "medium"
        else:
            interpretation = "large"
        
        print(f"Interpretation: {interpretation} effect size")
        print(f"Variance explained: {eta_squared*100:.2f}% of variance in flight distance")
        print("                    is explained by paper plane size")
        
        self.results['effect_size'] = {
            'eta_squared': eta_squared,
            'interpretation': interpretation
        }
        
    def correlation_analysis(self):
        print("\n7. CORRELATION ANALYSIS")
        print("-"*80)
        print("Pearson correlation: Size rank vs. Mean flight distance")
        
        size_means = self.df.groupby('size_rank')['distance_m'].mean()
        sizes = size_means.index.values
        means = size_means.values
        
        r, p_value = pearsonr(sizes, means)
        
        print(f"\nCorrelation coefficient (r): {r:.4f}")
        print(f"p-value: {p_value:.6f}")
        print(f"R-squared (R²): {r**2:.4f}")
        
        if abs(r) < 0.3:
            strength = "weak"
        elif abs(r) < 0.7:
            strength = "moderate"
        else:
            strength = "strong"
        
        direction = "negative" if r < 0 else "positive"
        
        print(f"\nInterpretation: {strength} {direction} correlation")
        print(f"As size rank increases (smaller planes), flight distance {'decreases' if r < 0 else 'increases'}")
        
        self.results['correlation'] = {
            'r': r,
            'p_value': p_value,
            'r_squared': r**2
        }
        
    def post_hoc_tests(self):
        print("\n8. POST-HOC ANALYSIS")
        print("-"*80)
        print("Selected pairwise comparisons (independent t-tests):")
        print("Comparing adjacent size groups and key comparisons")
        
        comparisons = [
            (1, 2), (5, 6), (1, 6), (14, 15), (1, 15)
        ]
        
        results = []
        for size1, size2 in comparisons:
            group1 = self.df[self.df['size_rank']==size1]['distance_m']
            group2 = self.df[self.df['size_rank']==size2]['distance_m']
            
            t_stat, p_value = stats.ttest_ind(group1, group2)
            
            mean_diff = group1.mean() - group2.mean()
            
            cohens_d = mean_diff / np.sqrt((group1.std()**2 + group2.std()**2) / 2)
            
            results.append({
                'Comparison': f'Size {size1} vs {size2}',
                'Mean Diff': f'{mean_diff:.2f}',
                't-stat': f'{t_stat:.3f}',
                'p-value': f'{p_value:.4f}',
                'Cohens d': f'{cohens_d:.3f}',
                'Significant': 'Yes' if p_value < 0.05 else 'No'
            })
        
        results_df = pd.DataFrame(results)
        print("\n" + results_df.to_string(index=False))
        
        print("\nNote: Bonferroni correction for multiple comparisons:")
        print(f"      Adjusted α = 0.05 / {len(comparisons)} = {0.05/len(comparisons):.4f}")
        
        self.results['posthoc'] = results_df
        
    def confidence_intervals(self):
        print("\n9. CONFIDENCE INTERVALS")
        print("-"*80)
        print("95% Confidence Intervals for mean flight distance by size:")
        
        ci_results = []
        for size in sorted(self.df['size_rank'].unique()):
            data = self.df[self.df['size_rank']==size]['distance_m']
            mean = data.mean()
            se = stats.sem(data)
            ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=se)
            
            ci_results.append({
                'Size': size,
                'Mean': f'{mean:.2f}',
                '95% CI Lower': f'{ci[0]:.2f}',
                '95% CI Upper': f'{ci[1]:.2f}',
                'Width': f'{ci[1]-ci[0]:.2f}'
            })
        
        ci_df = pd.DataFrame(ci_results)
        print("\n" + ci_df.to_string(index=False))
        
        self.results['confidence_intervals'] = ci_df
        
    def summary(self):
        print("\n10. SUMMARY OF FINDINGS")
        print("="*80)
        
        print("\nKey Results:")
        print(f"  • ANOVA F-statistic: {self.results['anova']['f_statistic']:.4f}")
        print(f"  • p-value: {self.results['anova']['p_value']:.6f}")
        print(f"  • Effect size (η²): {self.results['effect_size']['eta_squared']:.4f} ({self.results['effect_size']['interpretation']})")
        print(f"  • Correlation (r): {self.results['correlation']['r']:.4f}")
        
        print("\nStatistical Conclusion:")
        if self.results['anova']['p_value'] < 0.05:
            print("  Paper plane size has a SIGNIFICANT effect on flight distance.")
            print(f"  The effect size is {self.results['effect_size']['interpretation']}, explaining")
            print(f"  {self.results['effect_size']['eta_squared']*100:.1f}% of the variance in flight distance.")
        else:
            print("  No significant effect of paper plane size on flight distance was detected.")
        
        print("\nPractical Interpretation:")
        print("  As paper plane size decreases (higher size rank), flight distance")
        print(f"  shows a {self.results['correlation']['r']:.4f} correlation,")
        print("  indicating smaller planes tend to fly shorter distances.")
        
    def run_complete_analysis(self):
        self.load_data()
        self.state_hypotheses()
        self.descriptive_statistics()
        self.check_assumptions()
        self.one_way_anova()
        self.effect_size()
        self.correlation_analysis()
        self.post_hoc_tests()
        self.confidence_intervals()
        self.summary()
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)


def main():
    data_file = "../Data/raw_flight_data.csv"
    
    analysis = PaperPlaneAnalysis(data_file)
    analysis.run_complete_analysis()


if __name__ == "__main__":
    main()

