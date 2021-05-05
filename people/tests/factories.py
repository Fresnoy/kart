import factory

from utils.tests.factories import AndyFactory
from .. import models


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Artist

    user = factory.SubFactory(AndyFactory)
    nickname = "Andy Warhol"
