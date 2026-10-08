# 🎬 Netflix Content & Viewership Analysis

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)](#) [![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat&logo=pandas&logoColor=white)](#) [![SQL](https://img.shields.io/badge/SQL-Queries-4479A1?style=flat&logo=postgresql&logoColor=white)](#) [![Chart.js](https://img.shields.io/badge/Dashboard-Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)](#) [![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

An end-to-end analysis of Netflix with **two datasets**:

1. **Catalog (2008–2021):** 7,770 titles with director, cast, country, genre, rating, duration and description.
2. **Official viewership (Jul 2023 – Jun 2026):** hours viewed and views from Netflix's own *What We Watched* engagement reports.

🔗 **[Live Dashboard →](https://anjalisinghthakur.github.io/Netflix-data-analyst-project/dashboard/netflix_dashboard.html)**

| Catalog dashboard | Viewership dashboard |
|---|---|
| ![Catalog](images/09_catalog_dashboard.png) | ![Viewership](images/10_viewership_dashboard.png) |

---

## 📌 Questions answered
**Catalog:** Movies vs TV Shows over time? Which countries and genres dominate? How did content acquisition change by year and month? What does the rating mix say about the audience?
**Viewership:** Which titles got the most hours? How much viewing comes from new vs older titles? How do Movies and TV Shows compare? How did total viewing grow through 2026?

## 🗂️ Datasets

| Dataset | Source | Period | Size |
|---|---|---|---|
| Catalog | [Kaggle: Netflix Movies and TV Shows](https://www.kaggle.com/shivamb/netflix-shows) (mirrored via TidyTuesday) | titles added 2008–2021 | 7,787 raw → 7,770 clean |
| Viewership (title level) | Netflix *What We Watched* reports via [TidyTuesday 2025-07-29](https://github.com/rfordatascience/tidytuesday/tree/main/data/2025/2025-07-29) | Jul 2023 – Jun 2025 | 63,924 raw → 63,900 clean rows, 23,456 unique titles |
| Viewership (reported totals) | Netflix reports: [H1 2026](https://about.netflix.com/en/news/what-we-watched-the-first-half-of-2026), H2 2025, H1 2025 | Jan 2025 – Jun 2026 | totals + highlights only |

> **Limitation:** title-level data for Jul 2025 – Jun 2026 is not in this repo. Netflix publishes it as an Excel file on each report page; the dashboard uses Netflix's reported totals and named highlights for those two periods.

## 🛠️ Tech stack
Python · Pandas · NumPy · Matplotlib · Seaborn · SQL (SQLite/PostgreSQL) · HTML/CSS/Chart.js · Jupyter

## 📁 Project structure
```
├── README.md
├── DATA_AUDIT.md                        ← what was checked and fixed
├── requirements.txt
├── data/
│   ├── netflix_titles.csv               (catalog, raw)
│   ├── netflix_titles_cleaned.csv       (catalog, cleaned + features)
│   └── viewership/
│       ├── engagement_titles.csv        (official viewership, cleaned)
│       ├── reported_totals.csv          (Netflix-reported totals H1'25 – H1'26)
│       └── h1_2026_highlights.csv       (titles named in the H1 2026 report)
├── notebooks/
│   ├── netflix_analysis.ipynb · data_cleaning.py · eda_analysis.py   (catalog)
│   └── viewership_cleaning.py                                        (viewership)
├── sql/
│   ├── queries.sql                      (15 catalog queries)
│   └── viewership_queries.sql           (9 viewership queries)
├── dashboard/
│   ├── netflix_dashboard.html           (original summary dashboard)
│   ├── netflix_catalog_dashboard.html   (full 7,770-title explorer)
│   ├── netflix_viewership_dashboard.html(official viewership 2023–2026)
│   └── netflix_powerbi_style_dashboard.html
└── images/
```

## 🧹 Cleaning steps
**Catalog:** filled missing director/cast/country with "Not Specified" · dropped 17 rows missing `rating` (7) or `date_added` (10) · parsed dates · no duplicate titles · engineered `year_added`, `month_added`, `duration_value`, `primary_country`, `primary_genre`, `genre_count`, `days_release_to_add`.
**Viewership:** dropped 24 rows with no title or hours · kept the English title and the original-language title · converted hours/views to millions · parsed runtime to minutes · extracted premiere year · flagged global availability.

## 📈 Key insights: catalog (2008–2021)
- **Movies 69.1% (5,372) vs TV Shows 30.9% (2,398).** TV additions grew from 184 (2016) to 697 (2020). TV *share* is not a straight line: 41.8% (2016) → 25.5% (2018) → 34.7% (2020).
- **2019 was the peak year:** 2,153 titles added (1,497 movies, 656 shows).
- **United States** leads with 2,874 titles, then India (956) and the UK (576).
- **Dramas** is the most common *primary* genre (1,383). Counting *every* listed tag, International Movies leads (2,437), then Dramas (2,105).
- **TV-MA** is the top rating (2,861). Average movie runtime is **99.3 min**.
- **December** has the most additions (832); February the fewest (471).
- **Country counts:** 81 primary producing countries; 117 distinct countries when co-productions are counted.

## 📈 Key insights: official viewership (Jul 2023 – Jun 2026)
- Netflix reported **~95B hours (H1 2025), 96B (H2 2025) and 97B+ (H1 2026, a record)**.
- In the title-level data (Jul 2023 – Jun 2025): **373.3B hours** across 23,456 titles. **TV Shows drive 73%** of hours, Movies 27%.
- **Globally available titles generate 49%** of hours.
- Only **18% of hours** come from titles premiered in 2024 or later; older catalog is a large share.
- Most cumulative hours: *Squid Game: Season 2* (1,460M), *King the Land* (1,098M), *Bridgerton: Season 3* (985M).
- **KPop Demon Hunters** hit 482M views in H2 2025, the most-watched title ever in a six-month window. **War Machine** led H1 2026 with 147M views.
- Netflix moves from six-monthly to a **yearly** report starting Q1 2027.

## 🗃️ Sample SQL
```sql
-- Top 3 titles in every period (window function)
WITH ranked AS (
  SELECT period, title, hours_viewed_m,
         RANK() OVER (PARTITION BY period ORDER BY hours_viewed_m DESC) AS rnk
  FROM engagement)
SELECT period, rnk, title, hours_viewed_m FROM ranked WHERE rnk <= 3 ORDER BY period, rnk;
```

## ▶️ How to run
```bash
git clone https://github.com/AnjaliSinghThakur/Netflix-data-analyst-project.git
cd Netflix-data-analyst-project
pip install -r requirements.txt
jupyter notebook notebooks/netflix_analysis.ipynb      # catalog analysis
python notebooks/viewership_cleaning.py                # rebuild viewership CSV
# open any file in dashboard/ in your browser
```

## 🚀 Future improvements
- Add title-level data for Jul 2025 – Jun 2026 from Netflix's Excel reports
- Rebuild the dashboards in Power BI with DAX measures
- Join catalog and viewership data by title to compare genre vs hours viewed

*Built as a data analyst portfolio project: data cleaning, EDA, SQL and dashboards.*
