# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.utils.dateparse import parse_date

from production.models import Event, Film
from diffusion.models import Place

from people.tests.factories import ArtistFactory


class CommandsTestCase(TestCase):
    """
        Tests Production Models
    """

    def setUp(self):
        # create place
        self.place = Place(name="Le Fresnoy", description="Le Fresnoy Studio National", address="22 rue du Fresnoy")
        self.place.save()
        # create Artist
        self.artist = ArtistFactory()

    def tearDown(self):
        pass

    def test_event(self):
        "simple TEST create event"
        # create event
        self.event = Event(title='Panorama',
                           starting_date="1970-01-01 00:00:00.0+00:00",
                           type="EXIB",
                           place=self.place)
        self.event.save()
        # get Events
        events = Event.objects.all()
        # test metaEvent created
        self.assertEqual(events.count(), 1)

    def test_production_film(self):
        "simple TEST create film"
        film = Film(title="Diptyque Marilyn", production_date=parse_date("1962-01-01"))
        film.save()
        # set author
        film.authors.set((self.artist,))
        # get films
        films = Film.objects.all()
        # test film created
        self.assertEqual(films.count(), 1)
