#!/usr/bin/env python3
import csv
import statistics
from collections import defaultdict

def process_flight_data(input_file, output_file):
    print("=== Data Processing Script ===")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}\n")
    
    print("Step 1: Reading raw data...")
    raw_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append(row)
    print(f"Read {len(raw_data)} raw records\n")
    
    print("Step 2: Grouping by size...")
    grouped_data = defaultdict(list)
    for row in raw_data:
        size_rank = int(row['size_rank'])
        grouped_data[size_rank].append({
            'width_cm': float(row['width_cm']),
            'height_cm': float(row['height_cm']),
            'area_cm2': float(row['area_cm2']),
            'trial_number': int(row['trial_number']),
            'distance_m': float(row['distance_m'])
        })
    print(f"Grouped into {len(grouped_data)} sizes\n")
    
    print("Step 3: Calculating statistics...")
    processed_data = []
    for size_rank in sorted(grouped_data.keys()):
        trials = grouped_data[size_rank]
        
        trials_sorted = sorted(trials, key=lambda x: x['trial_number'])
        distances = [t['distance_m'] for t in trials_sorted]
        
        mean_distance = statistics.mean(distances)
        
        processed_row = {
            'size_rank': size_rank,
            'width_cm': trials[0]['width_cm'],
            'height_cm': trials[0]['height_cm'],
            'area_cm2': trials[0]['area_cm2'],
            'mean_m': round(mean_distance, 2)
        }
        
        for i, distance in enumerate(distances[:10], 1):
            processed_row[f'trial_{i}'] = distance
        
        processed_data.append(processed_row)
        print(f"  Size {size_rank}: {len(distances)} trials, mean = {mean_distance:.2f}m")
    
    print(f"\nProcessed {len(processed_data)} sizes\n")
    
    print("Step 4: Exporting processed data...")
    fieldnames = ['size_rank', 'width_cm', 'height_cm', 'area_cm2', 'mean_m',
                  'trial_1', 'trial_2', 'trial_3', 'trial_4', 'trial_5',
                  'trial_6', 'trial_7', 'trial_8', 'trial_9', 'trial_10']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)
    
    print(f"Data exported to: {output_file}\n")
    
    print("=== Processing Complete ===")
    print(f"Raw data: {len(raw_data)} rows (long format)")
    print(f"Processed data: {len(processed_data)} rows (wide format)")
    print(f"\nTransformations:")
    print(f"  - Long format to wide format")
    print(f"  - Calculated mean distances")
    print(f"  - Arranged 10 trials horizontally per size")


def main():
    input_file = "../Data/raw_flight_data.csv"
    output_file = "../Data/processed_flights_data.csv"
    
    process_flight_data(input_file, output_file)


if __name__ == "__main__":
    main()
