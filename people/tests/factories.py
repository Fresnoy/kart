import factory

from utils.tests.factories import UserFactory, AndyFactory
from .. import models


class FresnoyProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FresnoyProfile

    user = factory.SubFactory(UserFactory)


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Artist

    user = factory.SubFactory(UserFactory)
    nickname = factory.Faker('name')
    bio_short_fr = factory.Faker('paragraph')


class AndyArtistFactory(ArtistFactory):
    user = factory.SubFactory(AndyFactory)
    nickname = "Andy Warhol"


class StaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Staff

    user = factory.SubFactory(UserFactory)


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Organization

    name = factory.Faker('company')
    description = factory.Faker('paragraph')
