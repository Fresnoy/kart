# -*- encoding: utf-8 -*-
import sys

from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from diffusion.models import Place


def arg_to_unicode(bytestring):
    unicode_string = bytestring.decode(sys.getfilesystemencoding())
    return unicode_string


class Command(BaseCommand):
    help = 'Quickly create Place like: tourcoing france "22 place du Fresnoy"  '

    def add_arguments(self, parser):
        parser.add_argument('city', type=arg_to_unicode, help='City')
        parser.add_argument('country', type=arg_to_unicode, help='Country')

    def get_location(address):
        location = None
        try:
            geolocator = Nominatim(user_agent="place_create_app")
            location = geolocator.geocode(address, addressdetails=True)
        except GeocoderTimedOut:
            print 'Geocode timed out'
        return location

    def handle(self, *args, **options):

        city = options['city']
        country = options['country']

        try:
            # get or create duplicplaces (why?)
            place = Place.objects.get(name=city)
        except Exception:
            # Place doesnt'exist
            address = u"{0} {1}".format(city, country)
            location = self.get_location(address)
            if location is None:
                location = self.get_location(city)

            country_code = location.raw['address']['country_code'] if location else ""

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
