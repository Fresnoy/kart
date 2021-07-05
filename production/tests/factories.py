import factory
import factory.fuzzy

from django.utils import timezone
from taggit.models import Tag

from diffusion.tests.factories_alt import PlaceFactory
from people.tests.factories import StaffFactory, OrganizationFactory
from utils.tests.utils import first

from .. import models


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Task

    label = factory.Faker('sentence')
    description = factory.Faker('paragraph')


class StaffTaskFactory(TaskFactory):
    class Meta:
        model = models.StaffTask


class OrganizationTaskFactory(TaskFactory):
    class Meta:
        model = models.OrganizationTask


class ProductionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Production

    title = factory.Faker('sentence')


class ProductionStaffTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductionStaffTask

    staff = factory.SubFactory(StaffFactory)
    production = factory.SubFactory(ProductionFactory)
    task = factory.SubFactory(StaffTaskFactory)


class ProductionOrganizationTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductionOrganizationTask

    organization = factory.SubFactory(OrganizationFactory)
    production = factory.SubFactory(ProductionFactory)
    task = factory.SubFactory(OrganizationTaskFactory)


class ArtworkFactory(ProductionFactory):
    class Meta:
        model = models.Artwork

    production_date = factory.Faker('date_time_this_month', tzinfo=timezone.utc)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if extracted:
            # A list of authors were passed in, use them
            for author in extracted:
                self.authors.add(author)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word')
    slug = factory.Faker('slug')


class FilmGenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FilmGenre

    label = factory.Faker('sentence')


class FilmFactory(ArtworkFactory):
    class Meta:
        model = models.Film


class InstallationGenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InstallationGenre

    label = factory.Faker('sentence')


class InstallationFactory(ArtworkFactory):
    class Meta:
        model = models.Installation


class PerformanceFactory(ArtworkFactory):
    class Meta:
        model = models.Performance


class EventFactory(ProductionFactory):
    class Meta:
        model = models.Event

    type = factory.fuzzy.FuzzyChoice(models.Event.TYPE_CHOICES, getter=first)
    starting_date = factory.Faker('date_time_this_month', tzinfo=timezone.utc)
    place = factory.SubFactory(PlaceFactory)

    @factory.post_generation
    def subevents(self, create, extracted, **kwargs):
        if extracted:
            # A list of subevents were passed in, use them
            for subevent in extracted:
                self.subevents.add(subevent)


class ItineraryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Itinerary

    label_fr = factory.Faker('sentence')
    label_en = factory.Faker('sentence')
    description_fr = factory.Faker('paragraph')
    description_en = factory.Faker('paragraph')

    event = factory.SubFactory(EventFactory, type='EXHIB')


class ItineraryArtworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ItineraryArtwork

    itinerary = factory.SubFactory(ItineraryFactory)
    artwork = factory.SubFactory(ArtworkFactory)
    order = factory.Faker('random_int', max=5)
