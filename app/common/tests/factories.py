import factory
import factory.fuzzy

from utils.tests.utils import first

from .. import models


class WebsiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Website

    title_fr = factory.Faker('sentence')
    title_en = factory.Faker('sentence')
    language = factory.fuzzy.FuzzyChoice(models.Website.LANGUAGES, getter=first)
    url = factory.Faker('url')


class BTBeaconFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BTBeacon

    label = factory.Faker('name')
    uuid = factory.Faker('uuid4')
    rssi_in = factory.Faker('random_int')
    rssi_out = factory.Faker('random_int')
    x = factory.Faker('pyfloat')
    y = factory.Faker('pyfloat')
