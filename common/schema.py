from graphene_django import DjangoObjectType
from .models import Website
import graphene


class WebsiteType(DjangoObjectType):
    class Meta:
        model = Website


class Query(graphene.ObjectType):

    website = graphene.Field(WebsiteType, id=graphene.ID(required=True))
    websites = graphene.List(WebsiteType)
