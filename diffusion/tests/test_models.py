# -*- encoding: utf-8 -*-
import pytest

from django.test import TestCase

from production.models import Event
from diffusion.models import Place, MetaEvent


class CommandsTestCase(TestCase):
    """
        Tests Diffusion Commands
    """

    def setUp(self):
        # create place
        self.place = Place(name="Le Fresnoy", description="Le Fresnoy Studio National", address="22 rue du Fresnoy")
        self.place.save()
        # create event
        self.event = Event(title='PanoramaX',
                           starting_date="1970-01-01 00:00:00.0+00:00",
                           type="FEST",
                           place=self.place)
        self.event.save()
        # create meta_event
        self.main_event = Event(title='Panorama',
                                starting_date="1970-01-01 00:00:00.0+00:00",
                                type="EXIB",
                                main_event=True,
                                place=self.place)
        self.main_event.save()
        self.main_event.subevents.add(self.event)

    def tearDown(self):
        pass

    def test_meta_event(self):
        "simple TEST create meta_event"
        # create meta_event
        meta_event = MetaEvent(event=self.main_event, genres=['FILM'])
        meta_event.save()
        # get meta events
        meta_events = MetaEvent.objects.all()
        # test metaEvent created
        self.assertEqual(meta_events.count(), 1)
        parent_event = self.event.parent_event.first()
        # test parent event is main event
        self.assertEqual(parent_event.main_event, True)
        # test main event is meta event
        self.assertEqual(parent_event.meta_event.important, True)


@pytest.mark.django_db
class TestPlace:
    def test_str(self, place):
        place_str = str(place)
        assert place.name in place_str
        assert place.address[0:20] in place_str
        assert str(place.organization) in place_str

    def test_str_with_country(self, place):
        place.organization = None
        place.country = "FR"
        place.save()
        place_str = str(place)
        assert place.address[0:20] in place_str
        assert str(place.country) in place_str
        assert str(place.organization) not in place_str

    def test_str_without_address(self, place):
        # FIXME: conjonction peu probable, non ?
        place.name = place.address[0:20] + "..."
        place.save()
        place_str = str(place)

        assert place.name in place_str
        assert str(place.organization) in place_str


@pytest.mark.django_db
class TestMetaAward:
    def test_str(self, meta_award):
        meta_award_str = str(meta_award)
        assert meta_award.label in meta_award_str
        assert '(main event)' not in meta_award_str
        assert meta_award.event.title in meta_award_str
        assert str(meta_award.task) in meta_award_str

    def test_str_no_event(self, meta_award):
        meta_award.event = None
        meta_award.save()
        meta_award_str = str(meta_award)
        assert str(meta_award.task) in meta_award_str
        assert 'cat.' in meta_award_str

    def test_str_no_task(self, meta_award):
        meta_award.task = None
        meta_award.save()
        meta_award_str = str(meta_award)
        assert meta_award.event.title in meta_award_str
        assert 'cat.' not in meta_award_str


@pytest.mark.django_db
class TestAward:
    def test_str(self, award):
        award_str = str(award)
        assert str(award.date.year) in award_str
        assert str(award.meta_award) in award_str
        for artwork in award.artwork.all():
            assert str(artwork) in award_str


@pytest.mark.django_db
class TestMetaEvent:
    def test_str(self, meta_event):
        assert str(meta_event) == meta_event.event.title


@pytest.mark.django_db
class TestDiffusion:
    def test_str(self, diffusion):
        diffusion_str = str(diffusion)
        assert diffusion.artwork.title in diffusion_str
        assert diffusion.event.title in diffusion_str
