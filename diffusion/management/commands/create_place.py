# -*- encoding: utf-8 -*-
import sys

from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim

from diffusion.models import Place


def arg_to_unicode(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


class Command(BaseCommand):
    help = 'Quickly create Place like: tourcoing france "22 place du Fresnoy"  '

    def add_arguments(self, parser):
        parser.add_argument('city', type=arg_to_unicode, help='City')
        parser.add_argument('country', type=arg_to_unicode, help='Country')
        parser.add_argument('address', nargs="?", type=arg_to_unicode, help='set adress', default="")

    def handle(self, *args, **options):

        city = options['city']
        country = options['country']
        address = options['address']

        if address == "":
            address = u"{0} {1}".format(city, country)

        print(address)

        try:
            # get or create duplicplaces (why?)
            place = Place.objects.get(name=city, address=address)
        except Exception:
            # Place doesnt'exist
            if address == "":
                address = u"{0} {1}".format(city, country)
            print(address)

            geolocator = Nominatim(user_agent="place_create_app")
            location = geolocator.geocode(address, addressdetails=True)

            country_code = location.raw['address']['country_code'] if location else ""
            print("country_code")
            print(country_code)

            if location is None:
                location = geolocator.geocode(city)

            # print("location")
            # print(location)
            # print(city)

            place = Place(name=city,
                          description=city,
                          address=location.address,
                          latitude=location.latitude,
                          longitude=location.longitude,
                          city=city,
                          country=country_code,
                          )
            place.save()

        print(place)
