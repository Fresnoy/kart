import graphene
import operator
from functools import reduce

from graphene_django import DjangoObjectType

from django.db.models.functions import Concat
from django.db.models import Q, F, CharField

from .models import Gallery, Medium


class MediumType(DjangoObjectType):
    class Meta:
        model = Medium
    id = graphene.ID(required=True, source='pk')


def search_strings_in_model_colums(model, columns, strings):
    # l'idée est de réunir toutes les valeurs des colonnes recherchés en une seule (annotate)
    expr = [F(col) for col in columns]
    query = model.objects.annotate(fields_concat=Concat(*expr, output_field=CharField()))

    # et de tester si ces colonnes contiennent certains mots
    condition = reduce(operator.or_, [Q(fields_concat__icontains=s) for s in strings])
    return query.filter(condition)


def search_media_of_type(type):

    if(type == "audio"):
        columns = ["label", "description", "medium_url", "file"]
        audio_strings = ['audio', 'mp3', 'webm', 'aac', 'webm', 'soundcloud', 'deezer', 'spotify']
        query = search_strings_in_model_colums(Medium, columns, audio_strings)

    if(type == "picture" or type == "image"):
        columns = ["label", "description", "medium_url", "file", "picture"]
        picture_strings = ['image', 'jpg', 'jpeg', 'eps', 'psd', 'gif', 'png', 'tiff', 'svg', 'heic']
        query = search_strings_in_model_colums(Medium, columns, picture_strings)

    if(type == "video"):
        columns = ["label", "description", "medium_url", "file"]
        video_strings = ['mp4', 'ogg', 'vimeo', 'youtube']
        query = search_strings_in_model_colums(Medium, columns, video_strings)

    return query


class GalleryType(DjangoObjectType):
    class Meta:
        model = Gallery

    id = graphene.ID(required=True, source='pk')
    media = graphene.List(MediumType, media_type=graphene.String(required=False))

    def resolve_media(self, info, **kwargs):
        media_type = kwargs.get('media_type')
        if media_type is not None:
            query_media_type = search_media_of_type(media_type)
            return query_media_type.filter(gallery=self)

        return Medium.objects.all().filter(gallery=self)


class Query(graphene.ObjectType):

    gallery = graphene.Field(GalleryType, id=graphene.ID(required=True), media_type=graphene.String(required=False))

    medium = graphene.Field(MediumType, id=graphene.ID(required=True))
    media = graphene.List(MediumType, media_type=graphene.String(required=False))

    def resolve_media(self, info, **kwargs):
        media_type = kwargs.get('media_type')
        if media_type is not None:
            query_media_type = search_media_of_type(media_type)
            return query_media_type.filter(gallery=self)
        return Medium.objects.all().filter(gallery=self)
