from django.core.management.base import BaseCommand
from app1.tasks import run_visa_scraper

class Command(BaseCommand):
    help = 'Run the visa scraper task'

    def handle(self, *args, **kwargs):
        run_visa_scraper.delay()
        self.stdout.write(self.style.SUCCESS('Scraper task started'))
