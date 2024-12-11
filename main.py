from database_manager import init_db, save_tenders
from scripts.scraper import scrape_tenders

print("Initializing the database...")
init_db()

print("Scraping tenders from the website...")
tenders = scrape_tenders()

if tenders:
    print(f"Saving {len(tenders)} tenders to the database...")
    save_tenders(tenders)
    print("Tenders have been successfully saved to the database!")
else:
    print("No tenders found to save.")
