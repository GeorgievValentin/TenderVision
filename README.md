## A simple project for dara scraping from a public website

### Modules and Scripts
1. Scraper (scripts/scraper.py)
- Scrapes tender data from a public website.
- Handles pagination, scrolling, and error retries.
- Saves the data to the PostgreSQL database.
### Key Features
- Automatically navigates through all pages.
- Extracts data fields such as organization, deadline, and publish date.

2. Database Manager (database_manager.py)
- Handles interaction with the PostgreSQL database.
- Supports operations like saving, updating, and retrieving data.

3.Export to CSV (scripts/export_to_csv.py)
- Exports all tenders from the database to a CSV file.

4.Data Analysis (scripts/analyze_data.py)
- Loads the data from tenders.csv and performs analysis.
- Generates visualizations for:
  - Number of tenders by organization.
  - Tenders published by date.

5.Generate Report (scripts/generate_report.py)
- Generates a PDF report with key statistics and top 10 organizations by tenders.
### Key Features
- Summary of total tenders, top organizations, and date range.
- Lists the top 10 organizations by number of tenders.
