

import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower
import warnings
warnings.filterwarnings('ignore')


class StatisticalTester:
    
    def __init__(self, night_data, day_data, alpha=0.05):
        self.night_data = np.array(night_data)
        self.day_data = np.array(day_data)
        self.alpha = alpha
        
    def check_assumptions(self):
        print("\n" + "="*70)
        print("ASSUMPTION CHECKS")
        print("="*70)
        
        print("\n1. Normality Check (Shapiro-Wilk test on sample of 5000):")
        print("   Note: With large N, we rely on Central Limit Theorem")
        
        sample_size = min(5000, len(self.night_data), len(self.day_data))
        night_sample = np.random.choice(self.night_data, size=sample_size, replace=False)
        day_sample = np.random.choice(self.day_data, size=sample_size, replace=False)
        
        night_shapiro_stat, night_shapiro_p = stats.shapiro(night_sample)
        day_shapiro_stat, day_shapiro_p = stats.shapiro(day_sample)
        
        print(f"   Night: W={night_shapiro_stat:.4f}, p={night_shapiro_p:.4f}")
        print(f"   Day:   W={day_shapiro_stat:.4f}, p={day_shapiro_p:.4f}")
        
        if night_shapiro_p < 0.05 or day_shapiro_p < 0.05:
            print("   → Data significantly deviates from normality")
            print("   → But with N > 30,000, t-test is robust (CLT applies)")
        else:
            print("   → Data appears normally distributed")
        
        print("\n2. Homogeneity of Variance (Levene's test):")
        levene_stat, levene_p = stats.levene(self.night_data, self.day_data)
        print(f"   Statistic={levene_stat:.4f}, p={levene_p:.4f}")
        
        if levene_p < 0.05:
            print("   → Variances are significantly different")
            print("   → Will use Welch's t-test (does not assume equal variance)")
            self.equal_var = False
        else:
            print("   → Variances are approximately equal")
            print("   → Can use standard independent t-test")
            self.equal_var = True
        
        return {
            'normality_night_p': night_shapiro_p,
            'normality_day_p': day_shapiro_p,
            'levene_stat': levene_stat,
            'levene_p': levene_p,
            'equal_variance': self.equal_var
        }
    
    def calculate_effect_size(self):
        mean_diff = self.night_data.mean() - self.day_data.mean()
        
        n1, n2 = len(self.night_data), len(self.day_data)
        var1, var2 = self.night_data.var(ddof=1), self.day_data.var(ddof=1)
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        cohens_d = mean_diff / pooled_std
        
        if abs(cohens_d) < 0.2:
            interpretation = "negligible"
        elif abs(cohens_d) < 0.5:
            interpretation = "small"
        elif abs(cohens_d) < 0.8:
            interpretation = "medium"
        else:
            interpretation = "large"
        
        return cohens_d, interpretation
    
    def power_analysis(self, effect_size=None):
        print("\n" + "="*70)
        print("POWER ANALYSIS")
        print("="*70)
        
        if effect_size is None:
            effect_size, _ = self.calculate_effect_size()
            print(f"\nUsing observed effect size: d = {effect_size:.4f}")
        else:
            print(f"\nUsing specified effect size: d = {effect_size:.4f}")
        
        n1, n2 = len(self.night_data), len(self.day_data)
        ratio = n2 / n1
        
        print(f"Sample sizes: Night N={n1:,}, Day N={n2:,}")
        print(f"Significance level: α = {self.alpha}")
        
        power_analyzer = TTestIndPower()
        achieved_power = power_analyzer.solve_power(
            effect_size=abs(effect_size),
            nobs1=n1,
            ratio=ratio,
            alpha=self.alpha,
            alternative='two-sided'
        )
        
        print(f"\nAchieved Power: {achieved_power:.4f} ({achieved_power*100:.2f}%)")
        
        if achieved_power >= 0.8:
            print("✓ Power is adequate (≥ 0.80)")
        else:
            print("✗ Power is below recommended threshold (0.80)")
        
        mde = power_analyzer.solve_power(
            effect_size=None,
            nobs1=n1,
            ratio=ratio,
            alpha=self.alpha,
            power=0.8,
            alternative='two-sided'
        )
        
        print(f"\nMinimum Detectable Effect (80% power): d = {mde:.4f}")
        
        print("\nSample size needed per group for 80% power:")
        for d_val, d_name in [(0.2, 'small'), (0.5, 'medium'), (0.8, 'large')]:
            n_needed = power_analyzer.solve_power(
                effect_size=d_val,
                nobs1=None,
                ratio=1.0,
                alpha=self.alpha,
                power=0.8,
                alternative='two-sided'
            )
            print(f"  {d_name.capitalize()} effect (d={d_val}): N ≈ {int(np.ceil(n_needed)):,} per group")
        
        return {
            'effect_size': effect_size,
            'achieved_power': achieved_power,
            'mde': mde
        }
    
    def independent_t_test(self):
        print("\n" + "="*70)
        print("INDEPENDENT SAMPLES T-TEST")
        print("="*70)
        
        t_stat, p_value = stats.ttest_ind(
            self.night_data, 
            self.day_data, 
            equal_var=self.equal_var
        )
        
        mean_night = self.night_data.mean()
        mean_day = self.day_data.mean()
        mean_diff = mean_night - mean_day
        
        se_night = stats.sem(self.night_data)
        se_day = stats.sem(self.day_data)
        se_diff = np.sqrt(se_night**2 + se_day**2)
        
        if self.equal_var:
            df = len(self.night_data) + len(self.day_data) - 2
            test_type = "Standard Independent t-test"
        else:
            n1, n2 = len(self.night_data), len(self.day_data)
            s1, s2 = self.night_data.std(ddof=1), self.day_data.std(ddof=1)
            df = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
            test_type = "Welch's t-test (unequal variances)"
        
        ci_margin = stats.t.ppf(1 - self.alpha/2, df) * se_diff
        ci_lower = mean_diff - ci_margin
        ci_upper = mean_diff + ci_margin
        
        cohens_d, interpretation = self.calculate_effect_size()
        
        print(f"\nTest Type: {test_type}")
        print(f"\nHypotheses:")
        print(f"  H₀: μ_night = μ_day (no difference in mean casualties)")
        print(f"  H₁: μ_night ≠ μ_day (mean casualties differ)")
        print(f"\nDescriptive Statistics:")
        print(f"  Night mean: {mean_night:.4f} (SE = {se_night:.4f})")
        print(f"  Day mean:   {mean_day:.4f} (SE = {se_day:.4f})")
        print(f"  Mean difference: {mean_diff:.4f}")
        print(f"\nTest Statistics:")
        print(f"  t-statistic: {t_stat:.4f}")
        print(f"  Degrees of freedom: {df:.2f}")
        print(f"  p-value: {p_value:.6f}")
        print(f"\n95% Confidence Interval for mean difference:")
        print(f"  [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"\nEffect Size:")
        print(f"  Cohen's d: {cohens_d:.4f} ({interpretation} effect)")
        
        print(f"\nInterpretation:")
        if p_value < self.alpha:
            print(f"  ✓ p < {self.alpha}: REJECT the null hypothesis")
            print(f"  → There IS a statistically significant difference between")
            print(f"    night and day crash severity.")
            if mean_diff > 0:
                print(f"  → Night crashes have HIGHER average casualties than day crashes.")
            else:
                print(f"  → Day crashes have HIGHER average casualties than night crashes.")
        else:
            print(f"  ✗ p ≥ {self.alpha}: FAIL TO REJECT the null hypothesis")
            print(f"  → There is NO statistically significant difference between")
            print(f"    night and day crash severity.")
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'df': df,
            'mean_night': mean_night,
            'mean_day': mean_day,
            'mean_diff': mean_diff,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'cohens_d': cohens_d,
            'effect_interpretation': interpretation
        }
    
    def run_full_analysis(self):
        print("\n" + "="*70)
        print("STATISTICAL ANALYSIS: NIGHT vs DAY CRASH SEVERITY")
        print("="*70)
        
        assumptions = self.check_assumptions()
        
        power_results = self.power_analysis()
        
        test_results = self.independent_t_test()
        
        results = {
            'assumptions': assumptions,
            'power_analysis': power_results,
            'test_results': test_results
        }
        
        return results


if __name__ == "__main__":
    print("This module should be imported and used with real data.")
    print("See run_analysis.py for complete workflow.")

