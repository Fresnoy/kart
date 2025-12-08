from django.core.management.base import BaseCommand
import json

from production.management.commands.import_catalog import FIELD_MAPPING
# from ._import_diffusion.utils import (
#     createDiffusionEvents,
#     createDiffusionPlaces,
#     associateDiffusionEventsPlaces,
#     createDiffusions,
#     summary,
#     compareSummaries
# )
import pandas as pd
import requests
from datetime import datetime

from diffusion.models import Diffusion, Place


from production.utils import get_or_create_event
from utils.search_tools import input_choices

class Command(BaseCommand):
    help = "Import diffusion from CSV file or web JSON with mapping file -  ./manage.py import_diffusion"
    def add_arguments(self, parser):
        # Add csv file argument
        parser.add_argument(
            "--csvfile", type=str, default="", help="a diffusion csv file"
        )
        # Add json url argument
        parser.add_argument(
            "--jsonurl", type=str, default="", help="a diffusion json url"
        )
        
    def handle(self, *args, **options):
        csvfile = options["csvfile"]
        jsonurl = options["jsonurl"]

        if csvfile:
            df = pd.read_csv(csvfile)
        elif jsonurl:
            response = requests.get(jsonurl)
            data = response.json()
            df = pd.DataFrame(data)
        else:
            print("Please provide either --csvfile or --jsonurl argument.")
            return
        

        FIELD_MAPPING = {
            "name": "event__title",
            "start_date": "event__starting_date",
            "end_date": "event_ending_date",
            "type": "event__type",
            "place.name": "event__place__name",
            "place.address": "event__place__address",
            "place.city": "event__place__city",
            "place.country": "event__place__country",
            "place.latitude": "event__place__latitude", 
            "place.longitude": "event__place__longitude",
            "place.is_real_place": "is_real_place",
            "artworks": "artworks",
            # Add other necessary field mappings here
        }
        df = df.rename(columns=FIELD_MAPPING)

        print("Data imported. Number of records:", len(df))
        print("Columns:", df.columns.tolist())
        print(df.head())

        for index, row in df.iterrows():
            event_title = row.get("event__title")
            event_start_date = row.get("event__starting_date")
            
            event_end_date = row.get("event__ending_date")
            event_type = row.get("event__type")

            event = get_or_create_event(
                title=event_title,
                start_date=datetime.strptime(event_start_date, '%Y-%m-%d').date() if event_start_date else event_start_date,
                end_date=datetime.strptime(event_end_date, '%Y-%m-%d').date() if event_end_date else event_end_date,
                event_type=event_type
            )

            # print(f"Event processed: {event.title} ({event.starting_date} - {event.ending_date})")


            # place_name = row.get("event__place__name")
            # place_address = row.get("event__place__address")
            # place_city = row.get("event__place__city")
            # place_country = row.get("event__place__country")
            # place_latitude = row.get("event__place__latitude")
            # place_longitude = row.get("event__place__longitude")
            # is_real_place = row.get("is_real_place", True)

            # place, created = Place.objects.get_or_create(
            #     name=place_name,
            #     address=place_address,
            #     city=place_city,
            #     country=place_country,
            #     latitude=place_latitude,
            #     longitude=place_longitude,
            #     is_real_place=is_real_place
            # )

            # event.place = place
            # event.save()

            # diffusion = Diffusion.objects.create(
            #     event=event,
            #     artworks=row.get("artworks", "")
            # )

            print(f"Processed diffusion for event: {event_title}")

        # # Process the DataFrame to create diffusion entities
        
        # createDiffusions(df)

        # # Print summary
        # summary(df)
