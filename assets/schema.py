import graphene
from graphene_django import DjangoObjectType
from .models import Gallery, Medium


class MediumType(DjangoObjectType):
    class Meta:
        model = Medium


class GalleryType(DjangoObjectType):
    class Meta:
        model = Gallery

    media = graphene.List(MediumType)
