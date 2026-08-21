# StreamFlix — Dynamic Netflix Data Website

A Netflix-inspired dynamic frontend built on the project's existing `data/netflix_titles_cleaned.csv` dataset.

## Features

- Dynamic CSV-powered title library
- Search by title, cast, director and description
- Movie / TV Show filtering
- Genre, year and country filters
- Title details modal
- Surprise Me random title
- Persistent My List using localStorage
- Analytics summary and release-year chart
- Responsive Netflix-style dark UI

## Run locally

Because browsers block some local CSV requests when opening HTML directly, use a local web server.

### VS Code
Install **Live Server**, right-click `website/index.html`, then choose **Open with Live Server**.

### Python
From the repository root:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/website/`.

The existing analytics dashboard remains in `dashboard/netflix_dashboard.html`; this website is a separate frontend layer using the same project data.
