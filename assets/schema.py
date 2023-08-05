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

    def resolve_media(self, info):
        return Medium.objects.all().filter(gallery=self)


class Query(graphene.ObjectType):

    gallery = graphene.Field(GalleryType, id=graphene.ID(required=True))
    
    medium = graphene.Field(MediumType, id=graphene.ID(required=True))
    media = graphene.List(MediumType)