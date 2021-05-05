import factory

from .. import models


class WebsiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Website

    title_fr = "Site web d'Andy Warhol"
    title_en = "Andrew Warhol's Website"
    language = "EN"
    url = "https://www.warhol.org/"
