import factory

from .. import models


class GalleryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models. Gallery

    label = "Diptyque Marilyn"
    description = "Andrew Warhol's Artwork pictures"


class MediumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Medium

    gallery = factory.SubFactory(GalleryFactory)
    label = "Picture Diptyque Marilyn"
    description = "Color & Grey Marilyn"
