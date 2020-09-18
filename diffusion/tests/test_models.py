# -*- encoding: utf-8 -*-
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
