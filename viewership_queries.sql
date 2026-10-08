/* NETFLIX OFFICIAL VIEWERSHIP (What We Watched) - SQL QUERIES
   Table: engagement  (loaded from data/viewership/engagement_titles.csv)
   Columns: title, title_original, type, period, hours_viewed_m, views_m,
            runtime_min, release_date, premiere_year, available_globally
   Tested on SQLite. */

-- 1. Hours viewed per half-year, split by type (billions)
SELECT period, type, ROUND(SUM(hours_viewed_m)/1000.0, 1) AS hours_billion
FROM engagement GROUP BY period, type ORDER BY period, type;

-- 2. Top 10 titles by total hours across all periods
SELECT MIN(title) AS title, type, ROUND(SUM(hours_viewed_m)) AS hours_m, ROUND(SUM(views_m)) AS views_m
FROM engagement GROUP BY title_original, type ORDER BY hours_m DESC LIMIT 10;

-- 3. Top 3 titles in every period (window function)
WITH ranked AS (
  SELECT period, title, hours_viewed_m,
         RANK() OVER (PARTITION BY period ORDER BY hours_viewed_m DESC) AS rnk
  FROM engagement)
SELECT period, rnk, title, hours_viewed_m FROM ranked WHERE rnk <= 3 ORDER BY period, rnk;

-- 4. Share of hours by premiere-year bucket (new vs older catalog)
SELECT CASE WHEN premiere_year IS NULL THEN 'No date'
            WHEN premiere_year <= 2014 THEN '<=2014'
            ELSE CAST(premiere_year AS TEXT) END AS premiere_bucket,
       ROUND(SUM(hours_viewed_m)) AS hours_m,
       ROUND(100.0 * SUM(hours_viewed_m) / (SELECT SUM(hours_viewed_m) FROM engagement), 1) AS pct
FROM engagement GROUP BY premiere_bucket ORDER BY hours_m DESC;

-- 5. Global vs non-global titles: share of hours
SELECT CASE available_globally WHEN 1 THEN 'Global' ELSE 'Not global' END AS availability,
       ROUND(SUM(hours_viewed_m)) AS hours_m,
       ROUND(100.0 * SUM(hours_viewed_m) / (SELECT SUM(hours_viewed_m) FROM engagement), 1) AS pct
FROM engagement GROUP BY available_globally;

-- 6. Staying power: titles that appear in all 4 periods
SELECT MIN(title) AS title, type, COUNT(DISTINCT period) AS periods, ROUND(SUM(hours_viewed_m)) AS hours_m
FROM engagement GROUP BY title_original, type HAVING COUNT(DISTINCT period) = 4
ORDER BY hours_m DESC LIMIT 10;

-- 7. Movies vs TV Shows: average hours per title in each period
SELECT period, type, COUNT(*) AS titles, ROUND(AVG(hours_viewed_m), 1) AS avg_hours_m
FROM engagement GROUP BY period, type ORDER BY period, type;

-- 8. Unique titles in the dataset (a title = original-language name + type)
SELECT COUNT(*) AS unique_titles FROM (SELECT 1 FROM engagement GROUP BY title_original, type);

-- 9. Check against Netflix-reported totals (needs table reported_totals)
SELECT r.period, r.total_hours_billion AS reported_b,
       ROUND((SELECT SUM(hours_viewed_m) FROM engagement e WHERE e.period = r.period)/1000.0, 1) AS dataset_b
FROM reported_totals r;
