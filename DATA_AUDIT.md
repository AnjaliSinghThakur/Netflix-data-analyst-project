# Data Audit: project files vs dashboards

## ✅ Already matched (catalog files vs dashboards)
| Check | Files | Dashboard |
|---|---|---|
| Raw → clean rows | 7,787 → 7,770 (10 missing date + 7 missing rating) | 7,770 |
| Movies / TV Shows | 5,372 / 2,398 | 5,372 / 2,398 |
| Top country | United States 2,874 | 2,874 |
| Top primary genre | Dramas 1,383 | 1,383 |
| Top rating | TV-MA 2,861 | 2,861 |
| Peak year / month | 2019 (2,153) / December (832) | same |
| Avg movie runtime | 99.3 min | 99 |
| SQL | all 15 queries in `sql/queries.sql` run without errors on the cleaned CSV | n/a |

## ❌ Mismatches found and fixed
| # | Problem | Fix |
|---|---|---|
| 1 | README said *"TV Show share has grown steadily since 2016"*. Data says share went 41.8% (2016) → 25.5% (2018) → 34.7% (2020). It is the **count** that grew (184 → 697). | README and both earlier dashboards reworded. |
| 2 | Country count differed: **82** (Power BI-style dashboard), **81** (`dashboard_data.json`), **117** (full explorer). 82 wrongly included "Not Specified"; 117 counts co-production countries. | Defined both: **81 primary producing countries**, **117 distinct countries incl. co-productions**. Labels and numbers corrected. |
| 3 | "Top genre" differed: README says Dramas (first-listed genre); explorer showed International Movies (all tags). | Labelled clearly: *primary genre* vs *all genre tags*. |
| 4 | **No viewership data, SQL or script existed in the project** although the new dashboard uses it. | Added `data/viewership/` (3 CSVs), `viewership_cleaning.py`, `sql/viewership_queries.sql` (9 queries, all tested). |
| 5 | Unique-title count: dashboard 23,456 (original-language name) vs cleaning script 23,211 (English name only). | SQL now groups by `title_original` → 23,456. |
| 6 | Old README screenshot showed an outdated dashboard. | Added new screenshots (`images/09`, `images/10`) and README tables. |

## ✔ Viewership checks
- 63,924 raw rows → 63,900 clean (24 rows had no title or hours).
- Dataset sum for Jan–Jun 2025 = 95.2B hours vs Netflix-reported "over 95B".
- Global-title share of hours: 48.6% (dashboard shows 49%). Movie share 27%, titles premiered 2024+ 18%.

## ⚠ Known limitation
Title-level data for Jul 2025 – Jun 2026 is **not** in the project. Only Netflix-reported totals (96B, 97B+) and named highlights are included.
