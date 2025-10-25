

import sys
import os
from datetime import datetime

from analysis import CrashDataAnalyzer
from statistical_tests import StatisticalTester
from visualizations import CrashVisualizer


def print_header(title):
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80 + "\n")


def main():
    
    print_header("NYC MOTOR VEHICLE CRASH SEVERITY ANALYSIS")
    print("Research Question: Are nighttime crashes more severe than daytime crashes?")
    print("Hypothesis: Night crashes (18:00-05:59) have higher mean casualties than day crashes (06:00-17:59)")
    print(f"\nAnalysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    data_path = "/Users/leo/Desktop/510 Project 2/data/cleaned_final.csv"
    output_dir = "/Users/leo/Desktop/510 Project 2/results"
    figures_dir = "/Users/leo/Desktop/510 Project 2/figures"
    
    print_header("STEP 1: DATA LOADING AND PREPARATION")
    
    analyzer = CrashDataAnalyzer(data_path)
    df = analyzer.load_data()
    
    stats_df = analyzer.compute_descriptive_stats()
    
    processed_path = "/Users/leo/Desktop/510 Project 2/data/processed_data.csv"
    analyzer.save_processed_data(processed_path)
    
    print("\n" + "-"*70)
    print("HOURLY DISTRIBUTION SUMMARY")
    print("-"*70)
    hourly = analyzer.get_hourly_distribution()
    print(hourly.to_string(index=False))
    
    night_data = analyzer.night_data
    day_data = analyzer.day_data
    
    print_header("STEP 2: STATISTICAL ANALYSIS")
    
    tester = StatisticalTester(night_data, day_data, alpha=0.05)
    results = tester.run_full_analysis()
    
    print_header("STEP 3: GENERATING VISUALIZATIONS")
    
    visualizer = CrashVisualizer(df, night_data, day_data, output_dir=figures_dir)
    visualizer.create_all_visualizations(test_results=results['test_results'])
    
    print_header("STEP 4: ANALYSIS SUMMARY")
    
    test_res = results['test_results']
    power_res = results['power_analysis']
    
    print("KEY FINDINGS:")
    print("-" * 70)
    print(f"\n1. Sample Sizes:")
    print(f"   - Night crashes: {len(night_data):,}")
    print(f"   - Day crashes: {len(day_data):,}")
    
    print(f"\n2. Descriptive Statistics:")
    print(f"   - Night mean casualties: {test_res['mean_night']:.4f}")
    print(f"   - Day mean casualties: {test_res['mean_day']:.4f}")
    print(f"   - Mean difference: {test_res['mean_diff']:.4f}")
    
    print(f"\n3. Statistical Test Results:")
    print(f"   - Test: Independent samples t-test")
    print(f"   - t-statistic: {test_res['t_statistic']:.4f}")
    print(f"   - p-value: {test_res['p_value']:.6f}")
    print(f"   - 95% CI: [{test_res['ci_lower']:.4f}, {test_res['ci_upper']:.4f}]")
    
    print(f"\n4. Effect Size:")
    print(f"   - Cohen's d: {test_res['cohens_d']:.4f}")
    print(f"   - Interpretation: {test_res['effect_interpretation']} effect")
    
    print(f"\n5. Power Analysis:")
    print(f"   - Achieved power: {power_res['achieved_power']:.4f} ({power_res['achieved_power']*100:.2f}%)")
    print(f"   - Minimum detectable effect: {power_res['mde']:.4f}")
    
    print(f"\n6. Conclusion:")
    if test_res['p_value'] < 0.05:
        print(f"   ✓ REJECT H₀: Significant difference detected (p < 0.05)")
        if test_res['mean_diff'] > 0:
            print(f"   → Night crashes are MORE severe than day crashes")
        else:
            print(f"   → Day crashes are MORE severe than night crashes")
    else:
        print(f"   ✗ FAIL TO REJECT H₀: No significant difference (p ≥ 0.05)")
        print(f"   → Night and day crashes have similar severity")
    
    print_header("STEP 5: SAVING RESULTS")
    
    results_file = os.path.join(output_dir, "analysis_results.txt")
    
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("NYC MOTOR VEHICLE CRASH SEVERITY ANALYSIS RESULTS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("RESEARCH QUESTION\n")
        f.write("-"*80 + "\n")
        f.write("Are nighttime crashes more severe than daytime crashes in NYC?\n\n")
        
        f.write("HYPOTHESES\n")
        f.write("-"*80 + "\n")
        f.write("H₀: μ_night = μ_day (no difference in mean casualties)\n")
        f.write("H₁: μ_night ≠ μ_day (mean casualties differ)\n\n")
        
        f.write("SAMPLE SIZES\n")
        f.write("-"*80 + "\n")
        f.write(f"Night crashes (18:00-05:59): {len(night_data):,}\n")
        f.write(f"Day crashes (06:00-17:59): {len(day_data):,}\n\n")
        
        f.write("DESCRIPTIVE STATISTICS\n")
        f.write("-"*80 + "\n")
        f.write(stats_df.to_string(index=False))
        f.write("\n\n")
        
        f.write("STATISTICAL TEST RESULTS\n")
        f.write("-"*80 + "\n")
        f.write(f"Test: Independent samples t-test\n")
        f.write(f"t-statistic: {test_res['t_statistic']:.4f}\n")
        f.write(f"p-value: {test_res['p_value']:.6f}\n")
        f.write(f"Degrees of freedom: {test_res['df']:.2f}\n")
        f.write(f"95% Confidence Interval: [{test_res['ci_lower']:.4f}, {test_res['ci_upper']:.4f}]\n\n")
        
        f.write("EFFECT SIZE\n")
        f.write("-"*80 + "\n")
        f.write(f"Cohen's d: {test_res['cohens_d']:.4f}\n")
        f.write(f"Interpretation: {test_res['effect_interpretation']} effect\n\n")
        
        f.write("POWER ANALYSIS\n")
        f.write("-"*80 + "\n")
        f.write(f"Significance level (α): 0.05\n")
        f.write(f"Achieved power: {power_res['achieved_power']:.4f}\n")
        f.write(f"Minimum detectable effect (80% power): {power_res['mde']:.4f}\n\n")
        
        f.write("CONCLUSION\n")
        f.write("-"*80 + "\n")
        if test_res['p_value'] < 0.05:
            f.write(f"REJECT the null hypothesis (p = {test_res['p_value']:.6f} < 0.05)\n")
            if test_res['mean_diff'] > 0:
                f.write(f"Night crashes have significantly HIGHER average casualties than day crashes.\n")
                f.write(f"Mean difference: {test_res['mean_diff']:.4f} casualties per crash\n")
            else:
                f.write(f"Day crashes have significantly HIGHER average casualties than night crashes.\n")
                f.write(f"Mean difference: {abs(test_res['mean_diff']):.4f} casualties per crash\n")
        else:
            f.write(f"FAIL TO REJECT the null hypothesis (p = {test_res['p_value']:.6f} ≥ 0.05)\n")
            f.write(f"No statistically significant difference in crash severity between night and day.\n")
    
    print(f"Results saved to: {results_file}")
    
    print_header("ANALYSIS COMPLETE")
    
    print("Output Files:")
    print(f"  - Processed data: {processed_path}")
    print(f"  - Analysis results: {results_file}")
    print(f"  - Figures: {figures_dir}/")
    print(f"    • distribution_comparison.png")
    print(f"    • hourly_patterns.png")
    print(f"    • qq_plots.png")
    print(f"    • statistical_results.png")
    
    print(f"\nAnalysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nNext Steps:")
    print("  1. Review the analysis_results.txt file")
    print("  2. Examine all generated figures in the figures/ directory")
    print("  3. Use these results to complete your written report")
    print("  4. Prepare your presentation slides")
    
    return results


if __name__ == "__main__":
    try:
        results = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

