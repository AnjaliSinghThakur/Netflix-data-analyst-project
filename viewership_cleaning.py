"""Clean Netflix's official 'What We Watched' engagement reports (Jul 2023 - Jun 2025).
Source: TidyTuesday 2025-07-29 (mirror of Netflix's published engagement reports).
Run:  python notebooks/viewership_cleaning.py   ->  data/viewership/engagement_titles.csv"""
import pandas as pd, re
B = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-07-29/"
PERIODS = ["2023Jul-Dec", "2024Jan-Jun", "2024Jul-Dec", "2025Jan-Jun"]

def runtime_min(s):
    m = re.match(r"(?:(\d+)H)?\s*(?:(\d+)M)?", str(s))
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)

movies = pd.read_csv(B + "movies.csv").assign(type="Movie")
shows = pd.read_csv(B + "shows.csv").assign(type="TV Show")
df = pd.concat([movies, shows], ignore_index=True)
n0 = len(df)
df = df.dropna(subset=["title", "hours_viewed"])              # rows with no title / no hours
df["title_original"] = df["title"]
df["title"] = df["title"].str.split(" // ").str[0].str.strip()  # keep English title
df["period"] = df["report"]
df["hours_viewed_m"] = (df["hours_viewed"] / 1e6).round(1)
df["views_m"] = (df["views"].fillna(0) / 1e6).round(1)
df["runtime_min"] = df["runtime"].map(runtime_min)
df["available_globally"] = (df["available_globally"] == "Yes").astype(int)
df["premiere_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
cols = ["title", "title_original", "type", "period", "hours_viewed_m", "views_m",
        "runtime_min", "release_date", "premiere_year", "available_globally"]
df = df[cols].sort_values(["period", "hours_viewed_m"], ascending=[True, False])
df.to_csv("data/viewership/engagement_titles.csv", index=False)
print(f"{n0} raw rows -> {len(df)} clean rows ({n0-len(df)} dropped: missing title/hours)")
