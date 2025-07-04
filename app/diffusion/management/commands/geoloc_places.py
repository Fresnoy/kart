from django.core.management.base import BaseCommand
from ._import_awards.tools import geoloc_all_cities, compareSummaries, summary


class Command(BaseCommand):
    help = "Import awards from CSV file -  ./manage.py import_awards"

    def add_arguments(self, parser):

        # Add save argument
        parser.add_argument("--save", action="store_true", help="Save to db")
        # Add debug argument
        parser.add_argument("--debug", action="store_true", help="Debug mode")
        # Add Summary argument
        parser.add_argument("--summary", action="store_true", help="Summary mode")

    def handle(self, *args, **options):

        # Load arguments
        save = options["save"]
        debug = options["debug"]
        do_summary = options["summary"]

        if do_summary:
            # Snapshot of db state before process
            s1 = summary()

        # Trigger the geolocatisation of all places in the db
        geoloc_all_cities(save, debug)

        if do_summary:
            # Snapshot of db state after processes
            s2 = summary()

            # Compare the 2 snapshots
            comp = compareSummaries(s1, s2)

            # Display the amount of new content created
            self.stdout.write(self.style.SUCCESS(f"{comp}"))

        # Display confirmation message
        self.stdout.write(self.style.SUCCESS("Successfully geolocalised the places !"))
