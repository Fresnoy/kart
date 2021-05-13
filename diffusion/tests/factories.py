import factory

from django.utils import timezone

from people.tests.factories import OrganizationFactory
from production.tests.factories import ArtworkFactory, EventFactory, StaffTaskFactory
from utils.tests.utils import first

from .. import models


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Place

    name = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    address = factory.Faker('street_address')
    organization = factory.SubFactory(OrganizationFactory)


class MetaAwardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MetaAward

    label = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    type = factory.fuzzy.FuzzyChoice(models.MetaAward.TYPE_CHOICES, getter=first)
    event = factory.SubFactory(EventFactory, main_event=True)
    task = factory.SubFactory(StaffTaskFactory)


class AwardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Award

    meta_award = factory.SubFactory(MetaAwardFactory)
    event = factory.SubFactory(EventFactory)
    date = factory.Faker('date_time_this_year', tzinfo=timezone.utc)

    @factory.post_generation
    def artworks(self, create, extracted, **kwargs):
        if extracted:
            # A list of artworks were passed in, use them
            for artwork in extracted:
                self.artworks.add(artwork)
                for artist in artwork.authors.all():
                    self.artists.add(artist)

    @factory.post_generation
    def artists(self, create, extracted, **kwargs):
        if extracted:
            # A list of artists were passed in, use them
            for artist in extracted:
                self.artists.add(artist)


class MetaEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MetaEvent

    event = factory.SubFactory(EventFactory, main_event=True)


class DiffusionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Diffusion

    artwork = factory.SubFactory(ArtworkFactory)
    event = factory.SubFactory(EventFactory)
