/* =====================================================================
   NETFLIX CONTENT ANALYSIS - SQL QUERIES
   -----------------------------------------------------------------
   Table: netflix (loaded from netflix_titles_cleaned.csv)
   Columns used:
     show_id, type, title, director, cast, country, date_added,
     release_year, rating, duration, listed_in, description,
     year_added, month_added, duration_type, duration_value,
     primary_country, primary_genre, genre_count, days_release_to_add

   Tested on SQLite / PostgreSQL (minor syntax tweaks noted where relevant)
   ===================================================================== */


-- 1. Overall split of Movies vs TV Shows
SELECT
    type,
    COUNT(*) AS total_titles,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM netflix), 1) AS pct_of_catalog
FROM netflix
GROUP BY type
ORDER BY total_titles DESC;


-- 2. Content added per year, split by type
SELECT
    year_added,
    type,
    COUNT(*) AS titles_added
FROM netflix
GROUP BY year_added, type
ORDER BY year_added, type;


-- 3. Top 10 countries producing the most content
SELECT
    primary_country,
    COUNT(*) AS total_titles
FROM netflix
WHERE primary_country <> 'Not Specified'
GROUP BY primary_country
ORDER BY total_titles DESC
LIMIT 10;


-- 4. Top 5 genres per year using a WINDOW FUNCTION (RANK)
WITH genre_year_counts AS (
    SELECT
        year_added,
        primary_genre,
        COUNT(*) AS genre_count,
        RANK() OVER (
            PARTITION BY year_added
            ORDER BY COUNT(*) DESC
        ) AS genre_rank
    FROM netflix
    GROUP BY year_added, primary_genre
)
SELECT year_added, primary_genre, genre_count, genre_rank
FROM genre_year_counts
WHERE genre_rank <= 5
ORDER BY year_added, genre_rank;


-- 5. Most frequent directors (excluding "Not Specified")
SELECT
    director,
    COUNT(*) AS total_titles
FROM netflix
WHERE director <> 'Not Specified'
GROUP BY director
ORDER BY total_titles DESC
LIMIT 10;


-- 6. Content rating distribution
SELECT
    rating,
    COUNT(*) AS total_titles,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM netflix), 1) AS pct_of_catalog
FROM netflix
GROUP BY rating
ORDER BY total_titles DESC;


-- 7. Average movie duration by year of release
SELECT
    release_year,
    ROUND(AVG(duration_value), 1) AS avg_duration_minutes
FROM netflix
WHERE type = 'Movie'
GROUP BY release_year
ORDER BY release_year DESC
LIMIT 15;


-- 8. Titles that took longest to be added to Netflix after release (CTE + filter)
WITH release_gap AS (
    SELECT
        title,
        type,
        release_year,
        date_added,
        days_release_to_add
    FROM netflix
    WHERE days_release_to_add IS NOT NULL
)
SELECT *
FROM release_gap
ORDER BY days_release_to_add DESC
LIMIT 10;


-- 9. Month with the most content additions (seasonality)
SELECT
    month_added,
    COUNT(*) AS titles_added
FROM netflix
GROUP BY month_added
ORDER BY titles_added DESC;


-- 10. Running total of content added over time (WINDOW FUNCTION)
SELECT
    year_added,
    COUNT(*) AS titles_this_year,
    SUM(COUNT(*)) OVER (ORDER BY year_added) AS cumulative_titles
FROM netflix
GROUP BY year_added
ORDER BY year_added;


-- 11. Countries producing more TV Shows than Movies (HAVING clause)
SELECT
    primary_country,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count
FROM netflix
WHERE primary_country <> 'Not Specified'
GROUP BY primary_country
HAVING SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END)
       > SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END)
ORDER BY tv_show_count DESC;


-- 12. Titles with the most genres tagged (content complexity)
SELECT
    title,
    type,
    genre_count,
    listed_in
FROM netflix
ORDER BY genre_count DESC
LIMIT 10;


-- 13. Year-over-year growth rate in content additions
WITH yearly_totals AS (
    SELECT year_added, COUNT(*) AS total_titles
    FROM netflix
    GROUP BY year_added
)
SELECT
    year_added,
    total_titles,
    LAG(total_titles) OVER (ORDER BY year_added) AS prev_year_titles,
    ROUND(
        100.0 * (total_titles - LAG(total_titles) OVER (ORDER BY year_added))
        / NULLIF(LAG(total_titles) OVER (ORDER BY year_added), 0), 1
    ) AS pct_growth
FROM yearly_totals
ORDER BY year_added;


-- 14. TV-MA rated content by country (mature content concentration)
SELECT
    primary_country,
    COUNT(*) AS tv_ma_titles
FROM netflix
WHERE rating = 'TV-MA'
  AND primary_country <> 'Not Specified'
GROUP BY primary_country
ORDER BY tv_ma_titles DESC
LIMIT 10;


-- 15. Search titles by keyword in description (basic text search example)
SELECT title, type, release_year, description
FROM netflix
WHERE description LIKE '%family%'
ORDER BY release_year DESC
LIMIT 10;
