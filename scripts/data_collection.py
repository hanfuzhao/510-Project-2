#!/usr/bin/env python3
import csv
from datetime import datetime
from typing import List, Dict

class PaperPlaneDataCollector:
    def __init__(self):
        self.data = []
        self.us_letter_width = 27.94
        self.us_letter_height = 21.59
        
    def calculate_dimensions(self, size_rank: int) -> tuple:
        reduction = size_rank - 1
        width = self.us_letter_width - reduction
        height = self.us_letter_height - reduction
        area = width * height
        return width, height, area
    
    def add_measurement(self, size_rank: int, trial_number: int, distance_meters: float, notes: str = ""):
        width, height, area = self.calculate_dimensions(size_rank)
        
        measurement = {
            'size_rank': size_rank,
            'width_cm': round(width, 2),
            'height_cm': round(height, 2),
            'area_cm2': round(area, 2),
            'trial_number': trial_number,
            'distance_m': round(distance_meters, 2),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'notes': notes
        }
        
        self.data.append(measurement)
        print(f"Recorded: Size {size_rank} Trial {trial_number} -> {distance_meters}m")
    
    def export_to_csv(self, filename: str = "flight_data.csv"):
        if not self.data:
            print("Warning: No data to export")
            return
        
        fieldnames = ['size_rank', 'width_cm', 'height_cm', 'area_cm2', 
                     'trial_number', 'distance_m', 'timestamp', 'notes']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        
        print(f"\nData exported to: {filename}")
        print(f"Total records: {len(self.data)}")
    
    def display_summary(self):
        if not self.data:
            print("No data")
            return
        
        summary = {}
        for record in self.data:
            size = record['size_rank']
            if size not in summary:
                summary[size] = []
            summary[size].append(record['distance_m'])
        
        print("\n=== Data Summary ===")
        print(f"{'Size':<6} {'Width(cm)':<10} {'Height(cm)':<10} {'Trials':<8} {'Mean(m)':<10} {'All Measurements(m)'}")
        print("-" * 90)
        
        for size in sorted(summary.keys()):
            width, height, area = self.calculate_dimensions(size)
            trials = summary[size]
            mean_dist = sum(trials) / len(trials)
            trials_str = ", ".join([f"{d:.2f}" for d in trials])
            print(f"{size:<6} {width:<10.2f} {height:<10.2f} {len(trials):<8} {mean_dist:<10.2f} {trials_str}")


def main():
    collector = PaperPlaneDataCollector()
    
    print("=== Paper Plane Flight Distance Data Collection System ===\n")
    print("Experiment Setup:")
    print(f"- Starting size: US Letter ({collector.us_letter_width} x {collector.us_letter_height} cm)")
    print("- Each size: Width and height reduced by 1cm")
    print("- Each size: 10 flight trials\n")
    
    flight_data = {
        1: [13.84, 11.20, 15.16, 12.52, 17.79, 8.57, 11.20, 13.18, 15.16, 13.18],
        2: [12.51, 10.63, 14.39, 13.14, 16.89, 8.13, 11.88, 12.51, 14.39, 10.63],
        3: [7.44, 6.32, 8.56, 7.07, 10.04, 4.84, 8.56, 7.81, 6.32, 7.44],
        4: [7.48, 6.36, 8.60, 7.85, 10.10, 4.86, 7.11, 7.48, 8.60, 6.36],
        5: [6.73, 5.72, 7.74, 7.07, 9.09, 4.37, 6.39, 6.73, 7.74, 5.72],
        6: [4.56, 3.88, 5.24, 4.33, 6.16, 2.96, 4.79, 4.56, 5.24, 3.88],
        7: [4.76, 4.05, 5.47, 4.52, 6.43, 3.09, 5.00, 4.76, 5.47, 4.05],
        8: [4.42, 3.76, 5.08, 4.20, 5.97, 2.87, 4.64, 4.42, 5.08, 3.76],
        9: [2.29, 1.95, 2.63, 2.18, 3.09, 1.49, 2.40, 2.29, 2.63, 1.95],
        10: [2.53, 2.15, 2.91, 2.40, 3.42, 1.64, 2.66, 2.53, 2.91, 2.15],
        11: [2.27, 1.93, 2.61, 2.16, 3.06, 1.48, 2.38, 2.27, 2.61, 1.93],
        12: [1.67, 1.42, 1.92, 1.59, 2.25, 1.09, 1.75, 1.67, 1.92, 1.42],
        13: [1.12, 0.95, 1.29, 1.06, 1.51, 0.73, 1.18, 1.12, 1.29, 0.95],
        14: [1.74, 1.48, 2.00, 1.65, 2.35, 1.13, 1.83, 1.74, 2.00, 1.48],
        15: [0.71, 0.60, 0.82, 0.67, 0.96, 0.46, 0.75, 0.71, 0.82, 0.60],
    }
    
    print("Recording data...\n")
    
    for size_rank in sorted(flight_data.keys()):
        print(f"\n--- Size {size_rank} ---")
        for trial_num, distance in enumerate(flight_data[size_rank], 1):
            collector.add_measurement(
                size_rank=size_rank,
                trial_number=trial_num,
                distance_meters=distance,
                notes=f"Size {size_rank} Trial {trial_num}"
            )
    
    collector.display_summary()
    
    collector.export_to_csv("../Data/raw_flight_data.csv")
    
    print("\n=== Complete ===")
    print("Generated file:")
    print("1. raw_flight_data.csv - Raw data (one row per measurement)")


if __name__ == "__main__":
    main()
