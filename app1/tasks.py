from celery import shared_task
from .scraper import VisaScraper, Navigator, Parser, Saver

@shared_task
def run_visa_scraper():
    # Define the base URL
    base_url = "https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list"
    
    # Create instances of Navigator, Parser, and Saver
    navigator = Navigator(base_url)
    parser = Parser()
    saver = Saver()

    # Create a VisaScraper instance and run the scraper
    scraper = VisaScraper(navigator, parser, saver)
    scraper.run()
