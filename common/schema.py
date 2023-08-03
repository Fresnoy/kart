from graphene_django import DjangoObjectType
from .models import Website


class WebsiteType(DjangoObjectType):
    class Meta:
        model = Website
