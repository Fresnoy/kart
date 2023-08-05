from graphene_django import DjangoObjectType
from .models import Organization, Diffusion
import graphene


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
    id = graphene.ID(required=True, source='pk')


class DiffusionType(DjangoObjectType):
    class Meta:
        model = Diffusion
    id = graphene.ID(required=True, source='pk')


class Query(graphene.ObjectType):

    organization = graphene.Field(
        OrganizationType, id=graphene.ID(required=True))
    organizations = graphene.List(OrganizationType)

    diffusion = graphene.Field(DiffusionType, id=graphene.ID(required=True))
    diffusions = graphene.List(DiffusionType)
