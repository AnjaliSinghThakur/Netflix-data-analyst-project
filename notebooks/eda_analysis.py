"""
Netflix EDA - Exploratory Data Analysis
-----------------------------------------
Generates key charts and printed insights from the cleaned dataset.
Charts are saved to ../images/ for use in README and dashboard.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120

df = pd.read_csv("../data/netflix_titles_cleaned.csv", parse_dates=["date_added"])

# ------------------------------------------------------------------
# 1. Movies vs TV Shows split
# ------------------------------------------------------------------
type_counts = df["type"].value_counts()
plt.figure(figsize=(6, 5))
colors = ["#E50914", "#221f1f"]
plt.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%",
        colors=colors, startangle=90, textprops={"color": "white", "fontsize": 12})
plt.title("Movies vs TV Shows on Netflix", fontsize=14, weight="bold")
plt.tight_layout()
plt.savefig("../images/01_movies_vs_shows.png", facecolor="white")
plt.close()

# ------------------------------------------------------------------
# 2. Content added over the years
# ------------------------------------------------------------------
yearly = df.groupby(["year_added", "type"]).size().reset_index(name="count")
plt.figure(figsize=(10, 6))
sns.lineplot(data=yearly, x="year_added", y="count", hue="type",
             marker="o", palette=["#E50914", "#221f1f"], linewidth=2.5)
plt.title("Content Added to Netflix by Year", fontsize=14, weight="bold")
plt.xlabel("Year Added")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig("../images/02_content_by_year.png", facecolor="white")
plt.close()

# ------------------------------------------------------------------
# 3. Top 10 countries by content count
# ------------------------------------------------------------------
top_countries = (
    df[df["primary_country"] != "Not Specified"]["primary_country"]
    .value_counts()
    .head(10)
)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette="Reds_r")
plt.title("Top 10 Countries by Netflix Content", fontsize=14, weight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("../images/03_top_countries.png", facecolor="white")
plt.close()

# ------------------------------------------------------------------
# 4. Content rating distribution
# ------------------------------------------------------------------
rating_counts = df["rating"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=rating_counts.values, y=rating_counts.index, palette="rocket")
plt.title("Top 10 Content Ratings", fontsize=14, weight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("Rating")
plt.tight_layout()
plt.savefig("../images/04_rating_distribution.png", facecolor="white")
plt.close()

# ------------------------------------------------------------------
# 5. Top 10 genres
# ------------------------------------------------------------------
top_genres = df["primary_genre"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, palette="mako")
plt.title("Top 10 Genres on Netflix", fontsize=14, weight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("../images/05_top_genres.png", facecolor="white")
plt.close()

# ------------------------------------------------------------------
# 6. Movie duration distribution
# ------------------------------------------------------------------
movie_durations = df[df["type"] == "Movie"]["duration_value"]
plt.figure(figsize=(10, 6))
sns.histplot(movie_durations, bins=30, color="#E50914", kde=True)
plt.title("Movie Duration Distribution (minutes)", fontsize=14, weight="bold")
plt.xlabel("Duration (min)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("../images/06_movie_duration.png", facecolor="white")
plt.close()

# ------------------------------------------------------------------
# 7. Monthly content addition pattern
# ------------------------------------------------------------------
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
monthly = df["month_added"].value_counts().reindex(month_order)
plt.figure(figsize=(10, 6))
sns.barplot(x=monthly.index, y=monthly.values, palette="crest")
plt.title("Content Added by Month (All Years Combined)", fontsize=14, weight="bold")
plt.xlabel("Month")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../images/07_monthly_pattern.png", facecolor="white")
plt.close()

# ------------------------------------------------------------------
# Print key insights
# ------------------------------------------------------------------
print("=" * 60)
print("KEY INSIGHTS")
print("=" * 60)
print(f"Total titles analyzed: {len(df)}")
print(f"Movies: {type_counts.get('Movie', 0)} ({type_counts.get('Movie',0)/len(df)*100:.1f}%)")
print(f"TV Shows: {type_counts.get('TV Show', 0)} ({type_counts.get('TV Show',0)/len(df)*100:.1f}%)")
print(f"Top country: {top_countries.index[0]} ({top_countries.values[0]} titles)")
print(f"Top genre: {top_genres.index[0]} ({top_genres.values[0]} titles)")
print(f"Most common rating: {rating_counts.index[0]} ({rating_counts.values[0]} titles)")
print(f"Peak content-addition year: {yearly.groupby('year_added')['count'].sum().idxmax()}")
print(f"Average movie duration: {movie_durations.mean():.0f} minutes")
print(f"Busiest month for additions: {monthly.idxmax()}")
print("=" * 60)
print("All charts saved to ../images/")
