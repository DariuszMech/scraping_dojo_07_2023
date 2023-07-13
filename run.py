import os
from dotenv import load_dotenv
from scraping import QuoteScraper

load_dotenv()

if __name__ == "__main__":
    proxy = os.getenv("PROXY")
    url = os.getenv("INPUT_URL")
    output_file = os.getenv("OUTPUT_FILE")

    scraper = QuoteScraper(url, output_file)
    scraper.scrape_quotes()