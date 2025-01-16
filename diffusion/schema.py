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

    organization = graphene.Field(OrganizationType, id=graphene.ID(required=True))
    organizations = graphene.List(OrganizationType)

    diffusion = graphene.Field(DiffusionType, id=graphene.ID(required=True))
    diffusions = graphene.List(
        DiffusionType,
        eventTitleContains=graphene.String(),
        eventYear=graphene.Int(),
        placeStartWith=graphene.String(),
        artworkTitleContains=graphene.String(),
        artworkArtistNameStartWith=graphene.String(),
        orderBy=graphene.String(),
        limit=graphene.Int(),
    )

    place = graphene.Field(PlaceType, id=graphene.ID(required=True))
    places = graphene.List(PlaceType, placeStartWith=graphene.String())

    award = graphene.Field(AwardType, id=graphene.ID(required=True))
    awards = graphene.List(AwardType)

    meta_award = graphene.Field(MetaAwardType, id=graphene.ID(required=True))
    meta_awards = graphene.List(MetaAwardType)

    def resolve_organizations(root, info, **kwargs):
        return Organization.objects.all()

    def resolve_organization(root, info, **kwargs):
        id = kwargs.get('id', None)
        return Organization.objects.get(pk=id)

    def resolve_diffusions(
        root,
        info,
        eventTitleContains=None,
        eventPlaceStartWith=None,
        eventYear=None,
        artworkTitleContains=None,
        artworkArtistNameStartWith=None,
        orderBy=None,
        limit=None,
        **kwargs
    ):

        diffusion = Diffusion.objects.all()

        if eventTitleContains:
            diffusion = diffusion.filter(
                event__title__icontains=eventTitleContains,
            )

        if eventPlaceStartWith:
            diffusion = (
                diffusion.filter(
                    event__place__name__istartswith=eventPlaceStartWith,
                )
                | diffusion.filter(
                    event__place__city__istartswith=eventPlaceStartWith,
                )
                | diffusion.filter(
                    event__place__country__iexact=eventPlaceStartWith,
                )
                | diffusion.filter(
                    event__place__country__iname=eventPlaceStartWith,
                )
            )

        if artworkTitleContains:
            diffusion = diffusion.filter(
                artwork__title__icontains=artworkTitleContains,
            )

        if artworkArtistNameStartWith:
            diffusion = (
                diffusion.filter(artwork__authors__nickname__istartswith=artworkArtistNameStartWith)
                | diffusion.filter(artwork__authors__user__first_name__istartswith=artworkArtistNameStartWith)
                | diffusion.filter(artwork__authors__user__last_name__istartswith=artworkArtistNameStartWith)
            )

        if eventYear:
            diffusion = diffusion.filter(event__starting_date__year=eventYear)

        if orderBy:
            diffusion = diffusion.order_by(orderBy)

        if limit:
            diffusion = diffusion[:limit]

        return diffusion

    def resolve_diffusion(root, info, **kwargs):
        id = kwargs.get('id', None)
        return Diffusion.objects.get(pk=id)

    def resolve_places(root, info, **kwargs):
        placeStartWith = kwargs.get('placeStartWith')
        if placeStartWith:
            return (
                Place.objects.filter(
                    name__istartswith=placeStartWith,
                )
                | Place.objects.filter(
                    city__istartswith=placeStartWith,
                )
                | Place.objects.filter(
                    country__iexact=placeStartWith,
                )
                | Place.objects.filter(
                    country__iname=placeStartWith,
                )
            )
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
