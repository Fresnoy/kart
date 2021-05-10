import factory

from .. import models

from people.tests.factories import ArtistFactory


class PromotionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Promotion

    name = factory.Faker('catch_phrase')
    starting_year = factory.Faker('year')
    ending_year = factory.Faker('year')


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Student

    number = factory.Faker('random_int')
    promotion = factory.SubFactory(PromotionFactory)
    artist = factory.SubFactory(ArtistFactory)
    user = factory.SelfAttribute('artist.user')


class StudentApplicationSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentApplicationSetup

    name = factory.Faker('name')
    promotion = factory.SubFactory(PromotionFactory)
    candidature_date_start = factory.Faker('date_time_this_year', before_now=True, after_now=False)
    candidature_date_end = factory.Faker('date_time_this_year', before_now=False, after_now=True)
    date_of_birth_max = factory.Faker('date_of_birth', minimum_age=15)


class StudentApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentApplication

    artist = factory.SubFactory(ArtistFactory)
