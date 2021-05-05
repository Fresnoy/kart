import factory

from .. import models


class WebsiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Website

    title_fr = "Site web d'Andy Warhol"
    title_en = "Andrew Warhol's Website"
    language = "EN"
    url = "https://www.warhol.org/"


class BTBeaconFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BTBeacon

    label = factory.Faker('name')
    uuid = factory.Faker('uuid4')
    rssi_in = factory.Faker('random_int')
    rssi_out = factory.Faker('random_int')
    x = factory.Faker('pyfloat')
    y = factory.Faker('pyfloat')
