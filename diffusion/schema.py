from graphene_django import DjangoObjectType
from .models import Organization, Diffusion


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization


class DiffusionType(DjangoObjectType):
    class Meta:
        model = Diffusion
