import factory

from .. import models


class GalleryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Gallery

    label = factory.Faker('sentence')
    description = factory.Faker('paragraph')


class MediumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Medium

    gallery = factory.SubFactory(GalleryFactory)
    label = factory.Faker('sentence')
    description = factory.Faker('paragraph')
