import factory

from people.tests.factories import OrganizationFactory

from .. import models


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Place

    name = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    address = factory.Faker('street_address')
    organization = factory.SubFactory(OrganizationFactory)
