from django.core.management.base import BaseCommand
from ._import_awards.tools import createEvents, createPlaces, associateEventsPlaces, createAwards


class Command(BaseCommand):
    help = 'Import awards from CSV file -  ./manage.py import_awards'

    def handle(self, *args, **options):
        createEvents()
        createPlaces()
        associateEventsPlaces()
        createAwards()

        self.stdout.write(self.style.SUCCESS('Successfully imported the awards !'))
