"""
Netflix Data Cleaning Script
-----------------------------
Cleans the raw Netflix titles dataset and engineers new features
for downstream EDA, SQL analysis, and dashboarding.
"""

import pandas as pd
import numpy as np

# ------------------------------------------------------------------
# 1. Load raw data
# ------------------------------------------------------------------
df = pd.read_csv("../data/netflix_titles.csv")
print("Raw shape:", df.shape)

# ------------------------------------------------------------------
# 2. Handle missing values
# ------------------------------------------------------------------
df["director"] = df["director"].fillna("Not Specified")
df["cast"] = df["cast"].fillna("Not Specified")
df["country"] = df["country"].fillna("Not Specified")

# rating has very few nulls -> drop those rows
df = df.dropna(subset=["rating"])

# date_added has very few nulls -> drop those rows (needed for time trends)
df = df.dropna(subset=["date_added"])

# ------------------------------------------------------------------
# 3. Fix data types / formats
# ------------------------------------------------------------------
df["date_added"] = df["date_added"].str.strip()
df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y")

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month_name()

# ------------------------------------------------------------------
# 4. Remove duplicates
# ------------------------------------------------------------------
before = len(df)
df = df.drop_duplicates(subset=["title", "type", "release_year"])
print(f"Removed {before - len(df)} duplicate rows")

# ------------------------------------------------------------------
# 5. Feature engineering
# ------------------------------------------------------------------
# Split duration into numeric value + unit (movies = minutes, shows = seasons)
df["duration_type"] = np.where(df["type"] == "Movie", "min", "Season(s)")
df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(float)

# Primary country (first listed) — many rows have multiple countries
df["primary_country"] = df["country"].apply(lambda x: x.split(",")[0].strip())

# Primary genre (first listed category)
df["primary_genre"] = df["listed_in"].apply(lambda x: x.split(",")[0].strip())

# Number of genres per title
df["genre_count"] = df["listed_in"].apply(lambda x: len(x.split(",")))

# Days between release and added to Netflix (content "freshness")
df["days_release_to_add"] = (
    df["date_added"] - pd.to_datetime(df["release_year"], format="%Y")
).dt.days

# ------------------------------------------------------------------
# 6. Save cleaned dataset
# ------------------------------------------------------------------
df.to_csv("../data/netflix_titles_cleaned.csv", index=False)
print("Cleaned shape:", df.shape)
print("Saved to ../data/netflix_titles_cleaned.csv")
print(df.head())
