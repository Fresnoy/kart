from graphene_django import DjangoObjectType
from .models import Organization, Diffusion, Place, Award, MetaAward
import graphene


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
    id = graphene.ID(required=True, source='pk')
    places = graphene.List("diffusion.schema.PlaceType")

    def resolve_places(self, info):
        return Place.objects.all().filter(organization=self)


class DiffusionType(DjangoObjectType):
    class Meta:
        model = Diffusion
    id = graphene.ID(required=True, source='pk')


class AwardType(DjangoObjectType):
    class Meta:
        model = Award
    id = graphene.ID(required=True, source='pk')


class MetaAwardType(DjangoObjectType):
    class Meta:
        model = MetaAward
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

    place = graphene.Field(PlaceType, id=graphene.ID(required=True))
    places = graphene.List(PlaceType)

    award = graphene.Field(AwardType, id=graphene.ID(required=True))
    awards = graphene.List(AwardType)

    meta_award = graphene.Field(MetaAwardType, id=graphene.ID(required=True))
    meta_awards = graphene.List(MetaAwardType)

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

    def resolve_places(root, info, **kwargs):
        return Place.objects.all()

    def resolve_place(root, info, **kwargs):
        id = kwargs.get('id', None)
        return Place.objects.get(pk=id)

    def resolve_awards(root, info, **kwargs):
        return Award.objects.all()

    def resolve_award(root, info, **kwargs):
        id = kwargs.get('id', None)
        return Award.objects.get(pk=id)

    def resolve_meta_awards(root, info, **kwargs):
        return MetaAward.objects.all()

    def resolve_meta_award(root, info, **kwargs):
        id = kwargs.get('id', None)
        return MetaAward.objects.get(pk=id)
