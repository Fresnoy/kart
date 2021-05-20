# -*- encoding: utf-8 -*-
from django.core.management import call_command
from io import StringIO
from django.test import TestCase

from production.models import Event, Film
from people.tests.factories import ArtistFactory
from diffusion.models import Place, Diffusion


class CommandsTestCase(TestCase):
    """
        Tests Diffusion Commands
    """

    def setUp(self):
        # init command output
        self.out = StringIO()
        # create place
        self.place = Place(name="Le Fresnoy", description="Le Fresnoy Studio National", address="22 rue du Fresnoy")
        self.place.save()
        # create artist
        self.artist = ArtistFactory()
        self.artist.save()
        # create arwork
        self.film = Film(title="title", production_date="2019-01-01")
        self.film.save()
        self.film.authors.add(self.artist)
        self.film.save()
        # create event
        self.event = Event(title='PanoramaX',
                           starting_date="1970-01-01 00:00:00.0+00:00",
                           type="FEST",
                           place=self.place)
        self.event.save()
        self.event.films.add(self.film)
        self.event.save()

    def tearDown(self):
        pass

    def test_synchronize_diffusions(self):
        "simple TEST Command: synchronize_diffusion"
        call_command('synchronize_diffusions', stdout=self.out)
        diffusions = Diffusion.objects.all()
        self.assertEqual(diffusions.count(), 1)

    def test_place_creation(self):
        "simple TEST Command: create_place"
        call_command('create_city_place', 'Macondo', 'Colombia',
                     stdout=self.out)
        place = Place.objects.all()
        self.assertEqual(place.count(), 2)
