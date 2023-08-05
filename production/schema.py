import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field


from taggit.managers import TaggableManager
from itertools import chain

from .models import Production, Artwork, Film, Installation, \
    Performance, Event, Task, ProductionOrganizationTask


from people.schema import ArtistType, StaffType
from assets.schema import GalleryType
from common.schema import WebsiteType

from diffusion.models import Diffusion
from diffusion.schema import OrganizationType, DiffusionType


class ProductionInterface(graphene.Interface):
    id = graphene.ID(required=True, source='pk')
    title = graphene.String()
    former_title = graphene.String()
    subtitle = graphene.String()
    updated_on = graphene.Date()
    picture = graphene.String()
    websites = graphene.List(WebsiteType)
    collaborators = graphene.List(StaffType)
    partners = graphene.List(OrganizationType)
    description_short_fr = graphene.String()
    description_short_en = graphene.String()
    description_fr = graphene.String()
    description_en = graphene.String()

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Event):
            return EventType
        if isinstance(instance, Artwork):
            return ArtworkType
        else:
            return None  #


class ArtworkInterface(ProductionInterface):
    id = graphene.ID(required=True)

    # @classmethod
    # def is_type_of(cls, root, info):
    #     return isinstance(root, Artwork)
    authors = graphene.List(ArtistType)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Film):
            return FilmType
        if isinstance(instance, Performance):
            return PerformanceType
        if isinstance(instance, Installation):
            return InstallationType
        else:
            return None  #


class ProductionType(DjangoObjectType):
    class Meta:
        model = Production
        interfaces = (ProductionInterface, )

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Production)

    def resolve_partners(self, info, **kwargs):
        pots = ProductionOrganizationTask.objects.all().filter(production=self)
        partners = [pp.organization for pp in pots]
        return partners


class ArtworkType(ProductionType):
    class Meta:
        model = Artwork
        interfaces = (graphene.relay.Node, ProductionInterface)

    authors = graphene.List(ArtistType)

    # The type of artwork (Film, Performance, ...)
    type = graphene.String()

    # Galleries
    def resolve_gallery(self, info, galType=None):
        if galType == "process":
            return self.process_galleries.all()
        if galType == "mediation":
            return self.mediation_galleries.all()
        if galType == "insitu":
            return self.in_situ_galleries.all()
        if galType == "press":
            return self.press_galleries.all()
        if galType == "teaser":
            return self.teaser_galleries.all()
        return None

    processGalleries = graphene.List(
        GalleryType, resolver=resolve_gallery, galType=graphene.String(default_value="process"))

    mediationGalleries = graphene.List(
        GalleryType, resolver=resolve_gallery, galType=graphene.String(default_value="mediation"))

    inSituGalleries = graphene.List(
        GalleryType, resolver=resolve_gallery, galType=graphene.String(default_value="insitu"))

    pressGalleries = graphene.List(
        GalleryType, resolver=resolve_gallery, galType=graphene.String(default_value="press"))

    teaserGalleries = graphene.List(
        GalleryType, resolver=resolve_gallery, galType=graphene.String(default_value="teaser"))

    # Diffusions
    diffusions = graphene.List(DiffusionType)

    # Resolvers
    def resolve_type(self, info):
        if isinstance(self, Film):
            return "Film"
        if isinstance(self, Performance):
            return "Performance"
        if isinstance(self, Installation):
            return "Installation"

    def resolve_authors(self, info):
        return self.authors.all()

    def resolve_diffusions(self, info):
        return Diffusion.objects.all().filter(artwork=self)

    # Artworks by the same authors
    relArtworks = graphene.List(graphene.Int, aw_context=graphene.String())

    def resolve_relArtworks(self, info, aw_context="authors", **kwargs):
        ''' Related Artworks are artworks from same author'''
        if aw_context:
            if aw_context == "authors":
                auth = self.authors.all()
                aws = Artwork.objects.all().filter(authors__in=auth)
                return [aw.id for aw in aws if aw is not self]
        return None

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Artwork)

    @convert_django_field.register(TaggableManager)
    def convert_field_to_string(field, registry=None):
        return graphene.List(graphene.String, source='get_tags')


class ArtworkPanoType(ArtworkType):
    class Meta:
        model = Artwork
    """Deliver an artwork and the prev/next ones"""
    pass


class FilmType(ArtworkType):
    class Meta:
        model = Film
        interfaces = (graphene.relay.Node,
                      ProductionInterface, ArtworkInterface)

    duration = graphene.String()


class InstallationType(ArtworkType):
    class Meta:
        model = Installation
        interfaces = (graphene.relay.Node,
                      ProductionInterface, ArtworkInterface)


class PerformanceType(ArtworkType):
    class Meta:
        model = Performance
        interfaces = (graphene.relay.Node,
                      ProductionInterface, ArtworkInterface)


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        interfaces = (ProductionInterface,)

    artworks = graphene.List(
        ArtworkType, orderby=graphene.String(default_value="author"))
    artwork = graphene.Field(ArtworkType, id=graphene.ID(
    ))

    def resolve_artworks(self, info, orderby=None, **kwargs):

        # Collect all artworks
        aws = list(chain(self.installations.all(),
                   self.films.all(), self.performances.all()))

        if orderby:
            # Sort the artworks
            def tt(x):
                if orderby == "author":
                    art = x.authors.all().order_by('user__last_name').first().user.last_name
                if orderby == "title":
                    art = x.title
                return (art)

            aws = sorted(aws, key=lambda x: tt(x))
        return aws


class ExhibitionType(EventType):
    class Meta:
        model = Event


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class Query(graphene.ObjectType):

    production = graphene.Field(ProductionType, id=graphene.Int())
    productions = graphene.List(
        ProductionInterface, titleStartsWith=graphene.String())

    artwork = graphene.Field(ArtworkType, id=graphene.Int())
    artworks = graphene.List(ArtworkInterface)

    film = graphene.Field(FilmType, id=graphene.Int())
    films = graphene.List(FilmType)

    installation = graphene.Field(InstallationType, id=graphene.Int())
    installations = graphene.List(InstallationType)

    performance = graphene.Field(PerformanceType, id=graphene.Int())
    performances = graphene.List(PerformanceType)

    event = graphene.Field(EventType, id=graphene.Int())
    events = graphene.List(EventType)

    exhibition = graphene.Field(EventType, id=graphene.Int())
    exhibitions = graphene.List(EventType)

    task = graphene.Field(TaskType, id=graphene.Int())
    tasks = graphene.List(TaskType)

    # Production
    def resolve_productions(self, info, titleStartsWith=None, **kwargs):
        productions = Production.objects.all()

        if titleStartsWith:
            productions = productions.filter(
                title__istartswith=titleStartsWith)
            return productions
        return productions

    def resolve_production(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Production.objects.get(pk=id)
        return None

    # Artwork
    def resolve_artworks(self, info, **kwargs):
        return Artwork.objects.order_by('authors__last_name').all()

    def resolve_artwork(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Artwork.objects.get(pk=id)
        return None

    # Film
    def resolve_films(self, info, **kwargs):
        return Film.objects.all()

    def resolve_film(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Film.objects.get(pk=id)
        return None

    # Installation
    def resolve_installations(self, info, **kwargs):
        return Installation.objects.all()

    def resolve_installation(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Installation.objects.get(pk=id)
        return None

    # Performance
    def resolve_performances(self, info, **kwargs):
        return Performance.objects.all()

    def resolve_performance(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Performance.objects.get(pk=id)
        return None

    # Event
    def resolve_events(self, info, **kwargs):
        return Event.objects.all()

    def resolve_event(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Event.objects.get(pk=id)
        return None

    # Exhibition
    def resolve_exhibitions(self, info, **kwargs):
        return Event.objects.all()

    def resolve_exhibition(self, info, **kwargs):

        id = kwargs.get('id')
        if id is not None:
            return Event.objects.get(pk=id)
        return None

    # Task
    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_task(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Task.objects.get(pk=id)
        return None
