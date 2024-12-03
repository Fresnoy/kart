# -*- encoding: utf-8 -*-
import os

import datetime

from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from geopy.location import Location
from geopy.point import Point
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from diffusion.models import Place, Diffusion
from production.models import Artwork, Event


# Clear terminal
os.system('clear')


class Command(BaseCommand):
    help = 'Create diffusion step by step, no argument'

    def handle(self, *args, **options):

        init()


def init():

    # Clear terminal
    os.system('clear')

    print("Coller le texte de la diffusion")
    diff_text = input("")
    artwork = searchArtwork()
    artwork_type = artwork.polymorphic_ctype.name

    print("________")
    print(diff_text)
    print("________")

    event = search_or_create_Event()

    print("________")
    print(diff_text)
    print("________")

    diffusion = search_or_create_Diffusion(artwork=artwork, event=event)
    if diffusion:
        print("Diffusion crée : {} - {}".format(diffusion.id, diffusion))
        print("Ajout de l'œuvre {} à l'événement {}".format(artwork, event))
        # add artwork in event
        getattr(event, artwork_type + 's').add(artwork)
        event.save()

    print("FIN")
    exit = input("Créer une autre Diffusion ? y/n")
    if "n" in exit:
        os.exit()
    init()


def searchArtwork():

    artwork_str = input("L'œuvre : ")
    artwork_search = Artwork.objects.filter(title__icontains=artwork_str)
    artwork = input_choices(artwork_search)

    if not artwork:
        print("Aucune œuvre trouvée, veuiller retenter votre recherche ")
        return searchArtwork()

    print(artwork)
    return artwork


def search_or_create_Event():

    event_str = input("Recherche de l'événement : ")
    event_date = input("Date de l'événement aaaa-mm-jj (si périod ajouter / yyyy-mm-dd) ")
    ev_date_start = event_date.split("/")[0]
    event_search = (
        Event.objects.filter(title__icontains=event_str)
        | Event.objects.filter(place__name__icontains=event_str)
        | Event.objects.filter(starting_date=ev_date_start)
    )
    event = input_choices(event_search)

    if not event:
        print("Aucun événement trouvé, création")
        event = createEvent(event_str, event_date)

    return event


def search_or_create_Place():

    ev_place_str = input("Addresse de l'évènement : ")
    place_search = (
        Place.objects.filter(name__icontains=ev_place_str)
        | Place.objects.filter(description__icontains=ev_place_str)
        | Place.objects.filter(address__icontains=ev_place_str)
        | Place.objects.filter(city__icontains=ev_place_str)
    )

    place = input_choices(place_search)
    if not place:
        print("Aucune Place trouvée in DB, recheche externe")
        location_search = searchLocation(ev_place_str)
        location = input_choices(location_search)
        if location:

            city = (
                location.raw['address'].get('village')
                or location.raw['address'].get('town')
                or location.raw['address'].get('city')
            )

            country_code = location.raw['address'].get('country_code')

            place, created = Place.objects.get_or_create(
                name=ev_place_str,
                description=" ",
                address=location.address,
                longitude=location.longitude,
                latitude=location.latitude,
                city=city,
                country=country_code,
            )

            return place

        else:
            print("Aucune addresse trouvée, reformulez")
            return search_or_create_Place()

    return place


def createEvent(name, date):

    ev_name_str = input("Nom de l'événement : " + name + " ? ") or name
    ev_date_str = input("Date de l'événement (yyyy-mm-dd) (si périod ajouter / yyyy-mm-dd) : " + date + " ? ") or date

    ev_date_start = datetime.datetime.strptime(ev_date_str.split("/")[0], "%Y-%m-%d")
    ev_date_end = datetime.datetime.strptime(ev_date_str.split("/", 1)[1], "%Y-%m-%d") if "/" in ev_date_str else None

    place = search_or_create_Place()

    if place.event_set.all():
        print("Pour cet emplacement, plusieurs event possible")
        event = input_choices(place.event_set.all())
        if event:
            return event

    # no event finded
    # create it
    print("Type de l'événement")

    ev_type = input_choices(Event.TYPE_CHOICES)[0] or 'PROJ'
    event, created = Event.objects.get_or_create(
        title=ev_name_str, starting_date=ev_date_start, ending_date=ev_date_end, place=place, type=ev_type
    )

    return event


def input_choices(values):
    """
    Prompts the user to select a value from a list of choices.

    Args:
        values: A list of values to choose from.

    Returns:
        The selected value, or False if no valid choice was made.
    """

    if not values:
        return False

    print("Plusieurs valeurs sont possibles, selectionnez-en une :")
    for id, value in enumerate(values):
        print("{} : {}".format(id, value))

    select = input("Votre choix : ")

    try:
        select_int = int(select)
        selected = values[select_int]
        return selected
    except Exception as e:
        print("Choix invalide ")
        return False


def searchLocation(address):
    location = []
    try:
        geolocator = Nominatim(user_agent="place_create_app")
        location = geolocator.geocode(address, exactly_one=False, limit=5, addressdetails=True)
    except GeocoderTimedOut:
        print("Geocode timed out")
        location = geolocator.geocode(address, addressdetails=True)
    except GeocoderServiceError:
        # when travis test: no internet access
        print("GeocoderServiceError")
        location = []
    return location


def search_or_create_Diffusion(artwork, event):

    diffusion, created = Diffusion.objects.get_or_create(event=event, artwork=artwork)

    print("Première diffusion ? ")
    first = input_choices(Diffusion.FIRST_CHOICES) or [None]
    competition = True if "y" in input("En compétition ? y/n") else False

    diffusion.first = first[0]
    diffusion.on_competition = competition

    diffusion.save()

    return diffusion
