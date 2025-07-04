from django.core.management.base import BaseCommand
from ._import_awards.tools import (
    createEvents,
    createPlaces,
    associateEventsPlaces,
    createAwards,
    summary,
    compareSummaries
)
import pandas as pd


class Command(BaseCommand):
    help = "Import awards from CSV file -  ./manage.py import_awards"

    def add_arguments(self, parser):

        # Add csv file argument
        parser.add_argument(
            "--csvfile", type=str, default="", help="an awards csv file"
        )

    def handle(self, *args, **options):

        # Get the csvfile path from options
        csvfile = options["csvfile"]

        if csvfile == "":
            self.stdout.write(self.style.ERROR("A csv filepath must be provided (--csvfile)."))
            return

        # Snapshot of db state before process
        s1 = summary()

        # Generate a df from csv file path  TODO : generate df from with createEvents
        events_df = pd.read_csv(csvfile, delimiter=";")

        # Process chain to create awards
        createEvents(events_df, title_key="event_title")
        createPlaces()
        associateEventsPlaces()
        createAwards()

        # Snapshot of DB state after processes
        s2 = summary()

        # Compare the 2 snapshots
        comp = compareSummaries(s1, s2)

        # Display the amount of new content created
        self.stdout.write(self.style.SUCCESS(f"{comp}"))

        # Display confirmation message
        self.stdout.write(self.style.SUCCESS("Successfully imported the awards !"))
