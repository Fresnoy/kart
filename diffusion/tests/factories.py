import factory

from django.utils import timezone

from production.tests.factories import ArtworkFactory, EventFactory, StaffTaskFactory, TagFactory
from utils.tests.utils import first

from .. import models
from .factories_alt import PlaceFactory  # noqa


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
    def artwork(self, create, extracted, **kwargs):
        if extracted:
            # A list of artworks were passed in, use them
            for artwork in extracted:
                self.artwork.add(artwork)
                for artist in artwork.authors.all():
                    self.artist.add(artist.user)

    @factory.post_generation
    def artist(self, create, extracted, **kwargs):
        if extracted:
            # A list of artists were passed in, use them
            for artist in extracted:
                self.artist.add(artist.user)  # FIXME: artists are user?


class MetaEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MetaEvent

    event = factory.SubFactory(EventFactory, main_event=True)
    genres = factory.fuzzy.FuzzyChoice(models.MetaEvent.GENRES_CHOICES, getter=first)
    keywords = factory.SubFactory(TagFactory)


class DiffusionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Diffusion

    artwork = factory.SubFactory(ArtworkFactory)
    event = factory.SubFactory(EventFactory)
