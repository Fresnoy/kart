from graphene_django import DjangoObjectType
from .models import Organization, Diffusion, Place
import graphene


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
    id = graphene.ID(required=True, source='pk')


class DiffusionType(DjangoObjectType):
    class Meta:
        model = Diffusion
    id = graphene.ID(required=True, source='pk')


class PlaceType(DjangoObjectType):
    class Meta:
        model = Place


class Query(graphene.ObjectType):

    organization = graphene.Field(
        OrganizationType, id=graphene.ID(required=True))
    organizations = graphene.List(OrganizationType)

    diffusion = graphene.Field(DiffusionType, id=graphene.ID(required=True))
    diffusions = graphene.List(DiffusionType)

    def resolve_organizations(root, info, **kwargs):
        return Organization.objects.all()

    def resolve_organization(root, info, **kwargs):
        id = kwargs.get('id', None)
        return Organization.objects.get(pk=id)

    def resolve_diffusions(root, info, **kwargs):
        return Diffusion.objects.all()

    def resolve_diffusion(root, info, **kwargs):
        id = kwargs.get('id', None)
        return Diffusion.objects.get(pk=id)
