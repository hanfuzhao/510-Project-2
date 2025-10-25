# Data Files

Due to GitHub's 100MB file size limit, the data files are not included in this repository.

## How to Obtain the Data

### Original Raw Data
- **File**: `Motor_Vehicle_Collisions_-_Crashes.csv` (445 MB)
- **Source**: NYC Open Data
- **URL**: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
- **Instructions**: Download the CSV file and place it in this `data/` directory

### Processed Data
- **File**: `processed_data.csv` (188 MB)
- **Generation**: Run the following scripts in order:
  ```bash
  python scripts/data_clean.py
  python scripts/analysis.py
  ```
- This will create `processed_data.csv` with derived variables (crash_hour, total_casualties, time_period)

## Data Structure

After obtaining and processing the data, this directory should contain:
- `Motor_Vehicle_Collisions_-_Crashes.csv` - Raw data from NYC Open Data
- `processed_data.csv` - Cleaned and processed data ready for analysis

## Note

The analysis scripts are designed to work with the processed data. Make sure to generate it before running:
- `scripts/quick_analysis.py`
- `scripts/run_analysis.py`
- `scripts/create_visualizations.py`

