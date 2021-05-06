import factory

from utils.tests.factories import UserFactory, AndyFactory
from .. import models


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Artist

    user = factory.SubFactory(UserFactory)
    nickname = factory.Faker('name')


class AndyArtistFactory(ArtistFactory):
    user = factory.SubFactory(AndyFactory)
    nickname = "Andy Warhol"
