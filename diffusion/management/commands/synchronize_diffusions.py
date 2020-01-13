# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from production.models import Event, Artwork
from diffusion.models import Diffusion


class Command(BaseCommand):
    help = 'Synchronise Event artwork and Meta diffusion'

    def handle(self, *args, **options):
        events = Event.objects.filter(main_event=False)
        for event in events:
            artworks = []
            artworks.extend(event.films.all().values('id'))
            artworks.extend(event.installations.all().values('id'))
            artworks.extend(event.performances.all().values('id'))
            print(f"Event: {event.title.encode('utf-8')}")
            #
            for aw in artworks:
                artwork = Artwork.objects.get(id=aw['id'])
                try:
                    diffusion = Diffusion.objects.get(event=event, artwork=artwork)
                except Exception:
                    diffusion = Diffusion(event=event, artwork=artwork)
                    diffusion.save()
                    print("  Create diff: ", artwork)
