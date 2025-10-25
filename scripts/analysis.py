

import pandas as pd
import numpy as np
from datetime import datetime, time


class CrashDataAnalyzer:
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.night_data = None
        self.day_data = None
        
    def load_data(self):
        print("Loading cleaned data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df):,} records")
        
        self.df['crash_hour'] = pd.to_datetime(
            self.df['crash_time'], 
            format='%H:%M', 
            errors='coerce'
        ).dt.hour
        
        self.df['total_casualties'] = (
            self.df['number_of_persons_injured'] + 
            self.df['number_of_persons_killed']
        )
        
        self.df['time_period'] = self.df['crash_hour'].apply(
            lambda h: 'Night' if (h >= 18 or h < 6) else 'Day'
        )
        
        self.night_data = self.df[self.df['time_period'] == 'Night']['total_casualties']
        self.day_data = self.df[self.df['time_period'] == 'Day']['total_casualties']
        
        print(f"\nTime period classification:")
        print(f"  Night crashes (18:00-05:59): {len(self.night_data):,}")
        print(f"  Day crashes (06:00-17:59): {len(self.day_data):,}")
        
        return self.df
    
    def compute_descriptive_stats(self):
        if self.night_data is None or self.day_data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        print("\n" + "="*70)
        print("DESCRIPTIVE STATISTICS")
        print("="*70)
        
        stats_dict = {
            'Group': ['Night (18:00-05:59)', 'Day (06:00-17:59)'],
            'N': [len(self.night_data), len(self.day_data)],
            'Mean': [self.night_data.mean(), self.day_data.mean()],
            'Std': [self.night_data.std(), self.day_data.std()],
            'Median': [self.night_data.median(), self.day_data.median()],
            'Min': [self.night_data.min(), self.day_data.min()],
            'Max': [self.night_data.max(), self.day_data.max()],
            'Q1': [self.night_data.quantile(0.25), self.day_data.quantile(0.25)],
            'Q3': [self.night_data.quantile(0.75), self.day_data.quantile(0.75)]
        }
        
        stats_df = pd.DataFrame(stats_dict)
        print(stats_df.to_string(index=False))
        
        mean_diff = self.night_data.mean() - self.day_data.mean()
        print(f"\nMean Difference (Night - Day): {mean_diff:.4f}")
        
        night_with_casualties = (self.night_data > 0).sum()
        day_with_casualties = (self.day_data > 0).sum()
        
        print(f"\nCrashes with casualties (injured or killed > 0):")
        print(f"  Night: {night_with_casualties:,} ({100*night_with_casualties/len(self.night_data):.2f}%)")
        print(f"  Day: {day_with_casualties:,} ({100*day_with_casualties/len(self.day_data):.2f}%)")
        
        return stats_df
    
    def get_hourly_distribution(self):
        hourly_stats = self.df.groupby('crash_hour').agg({
            'total_casualties': ['count', 'sum', 'mean', 'std']
        }).round(4)
        
        hourly_stats.columns = ['Crash_Count', 'Total_Casualties', 'Mean_Casualties', 'Std_Casualties']
        hourly_stats = hourly_stats.reset_index()
        
        return hourly_stats
    
    def save_processed_data(self, output_path):
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        self.df.to_csv(output_path, index=False)
        print(f"\nProcessed data saved to: {output_path}")


if __name__ == "__main__":
    analyzer = CrashDataAnalyzer("/Users/leo/Desktop/510 Project 2/data/cleaned_final.csv")
    analyzer.load_data()
    analyzer.compute_descriptive_stats()
    
    analyzer.save_processed_data("/Users/leo/Desktop/510 Project 2/data/processed_data.csv")
    
    print("\n" + "="*70)
    print("HOURLY DISTRIBUTION")
    print("="*70)
    hourly = analyzer.get_hourly_distribution()
    print(hourly.to_string(index=False))

