
import pandas as pd
import numpy as np
import re

in_path  = "/Users/leo/Desktop/510 Project 2/data/Motor_Vehicle_Collisions_-_Crashes.csv"
out_path = "/Users/leo/Desktop/510 Project 2/data/cleaned_final.csv"

print("Loading dataset ...")
df = pd.read_csv(in_path, header=0, low_memory=False)
print(f"Raw shape: {df.shape}")

def norm(c):
    c = str(c).strip().lower()
    c = re.sub(r"[^0-9a-z]+", "_", c)
    c = re.sub(r"_+", "_", c).strip("_")
    return c

df.columns = [norm(c) for c in df.columns]

if "collision_id" in df.columns:
    df["collision_id"] = df["collision_id"].astype(str)

valid_cols = [c for c in df.columns if not c.startswith("unnamed")]
if len(valid_cols) != len(df.columns):
    df = df[valid_cols]
    print(f"Dropped unnamed trailing columns. New shape: {df.shape}")

cols_to_drop = [
    "off_street_name",
    "contributing_factor_vehicle_3",
    "contributing_factor_vehicle_4",
    "contributing_factor_vehicle_5",
    "latitude",
    "longitude",
    "location",
]
existing_drop = [c for c in cols_to_drop if c in df.columns]
df = df.drop(columns=existing_drop, errors="ignore")
print(f"🗑️ Dropped columns: {existing_drop}")

veh_cols = [c for c in df.columns if c in [
    "vehicle_type_code_1",
    "vehicle_type_code_2",
    "vehicle_type_code_3",
    "vehicle_type_code_4",
    "vehicle_type_code_5",
]]
print(f"Vehicle type columns (excluded from emptiness rule): {veh_cols}")

df = df.replace(r"^\s*$", np.nan, regex=True)

nonveh_cols = [c for c in df.columns if c not in veh_cols]
before = len(df)
df = df.dropna(subset=nonveh_cols, how="any").reset_index(drop=True)
print(f"Dropped {before - len(df):,} rows due to empties in NON-vehicle columns. Kept: {len(df):,}")

df["crash_date"] = pd.to_datetime(df["crash_date"], errors="coerce")

def combine_dt(date, time_str):
    if pd.isna(date) or pd.isna(time_str):
        return pd.NaT
    try:
        return pd.to_datetime(f"{date} {time_str}", errors="coerce")
    except Exception:
        return pd.NaT

print("Sorting by crash_date + crash_time (oldest → newest) ...")
df["_sort_key"] = [combine_dt(d, t) for d, t in zip(df["crash_date"], df.get("crash_time", ""))]
bad = df["_sort_key"].isna().sum()
if bad:
    print(f"Dropping {bad} rows with invalid date/time for sorting.")
df = df[df["_sort_key"].notna()].sort_values("_sort_key").reset_index(drop=True)
df = df.drop(columns=["_sort_key"])

df.to_csv(out_path, index=False)
print(f"Cleaned dataset saved to: {out_path}")
print(f"Final shape: {df.shape}")
print(df.head(10))
