import factory

from django.utils import timezone

from people.tests.factories import ArtistFactory, OrganizationFactory, UserFactory

from .. import models


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


class PhdStudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PhdStudent
    student = factory.SubFactory(StudentFactory)
    university = factory.SubFactory(OrganizationFactory)
    director = factory.SubFactory(UserFactory)
    thesis_object = factory.Faker('word')


class ScientificStudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ScientificStudent
    student = factory.SubFactory(StudentFactory)
    discipline = factory.Faker('word')


class TeachingArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TeachingArtist
    artist = factory.SubFactory(ArtistFactory)
    presentation_text_fr = factory.Faker('word')
    presentation_text_en = factory.Faker('word')


class StudentApplicationSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentApplicationSetup

    name = factory.Faker('name')
    promotion = factory.SubFactory(PromotionFactory)
    candidature_date_start = factory.Faker('date_time_this_year', before_now=True, after_now=False, tzinfo=timezone.utc)
    candidature_date_end = factory.Faker('date_time_this_year', before_now=False, after_now=True, tzinfo=timezone.utc)
    date_of_birth_max = factory.Faker('date_of_birth', minimum_age=15, tzinfo=timezone.utc)
    interviews_start_date = factory.SelfAttribute('candidature_date_end')
    interviews_end_date = factory.SelfAttribute('candidature_date_end')


class StudentApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StudentApplication

    artist = factory.SubFactory(ArtistFactory)
    campaign = factory.SubFactory(StudentApplicationSetupFactory)
