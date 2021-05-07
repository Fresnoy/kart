# -*- encoding: utf-8 -*-
import pytest

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


@pytest.mark.django_db
class TestStaffTask:
    def test_str(self, staff_task):
        assert staff_task.label == str(staff_task)


@pytest.mark.django_db
class TestProductionStaffTask:
    def test_str(self, production_staff_task):
        production_staff_task_str = str(production_staff_task)
        assert production_staff_task.task.label in production_staff_task_str
        assert production_staff_task.production.title in production_staff_task_str


@pytest.mark.django_db
class TestProduction:
    def test_str(self, production):
        assert production.title == str(production)


@pytest.mark.django_db
class TestArtwork:
    def test_str(self, artwork):
        artwork_str = str(artwork)
        assert artwork.title in artwork_str
        assert str(artwork.production_date.year) in artwork_str
        assert str(artwork.authors.last()) in artwork_str

    def test_anonymous_str(self, anonymous_artwork):
        assert str(anonymous_artwork).endswith("de ?")


@pytest.mark.django_db
class TestFilmGenre:
    def test_str(self, film_genre):
        assert film_genre.label == str(film_genre)


@pytest.mark.django_db
class TestInstallationGenre:
    def test_str(self, installation_genre):
        assert installation_genre.label == str(installation_genre)


@pytest.mark.django_db
class TestEvent:
    def test_str(self, event):
        event_str = str(event)
        assert event.title in event_str
        assert str(event.starting_date.year) in event_str

    def test_main_event_str(self, main_event):
        main_event_str = str(main_event)
        assert main_event.title in main_event_str
        assert str(main_event.starting_date.year) not in main_event_str

    def test_sub_event_str(self, main_event):
        subevent = main_event.subevents.last()
        subevent_str = str(subevent)
        assert subevent.title in subevent_str
        assert main_event.title in subevent_str
        assert str(subevent.starting_date.year) not in subevent_str


@pytest.mark.django_db
class TestItinerary:
    def test_str(self, itinerary):
        itinerary_str = str(itinerary)
        assert itinerary.label_fr in itinerary_str
        assert itinerary.event.title in itinerary_str
