import graphene
from graphene_django import DjangoObjectType

from graphene_django.converter import convert_django_field
from taggit.managers import TaggableManager

from .models import Production, Artwork, Film, Installation, \
    Performance, Event, Task

from people.schema import ArtistType
from assets.schema import GalleryType
from diffusion.schema import OrganizationType, DiffusionType


class ProductionInterface(graphene.Interface):
    id = graphene.ID(required=True)


class ProductionType(DjangoObjectType):
    class Meta:
        model = Production

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Production)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Film):
            return FilmType
        elif isinstance(instance, Performance):
            return PerformanceType
        elif isinstance(instance, Artwork):
            return ArtworkType
        # Ajoutez d'autres conditions pour les autres sous-types d'Artwork ici
        else:
            return None  #

    __typename = graphene.String()
    def resolve___typename():
        return "coucou"
    

    partners = graphene.List(OrganizationType)


class ArtworkType(ProductionType):
    class Meta:
        model = Artwork
        interfaces = (graphene.relay.Node, ProductionInterface)

    authors = graphene.List(ArtistType)

    # The type of artwork (Film, Performance, ...)
    type = graphene.String()

    # Galleries
    process_galleries = graphene.List(GalleryType)
    mediation_galleries = graphene.List(GalleryType)
    in_situ_galleries = graphene.List(GalleryType)
    press_galleries = graphene.List(GalleryType)
    teaser_galleries = graphene.List(GalleryType)

    # Diffusions
    diffusions = graphene.List(DiffusionType)

    def resolve_type(self, info):
        if isinstance(self, Film):
            return "Film"
        if isinstance(self, Performance):
            return "Performance"
        if isinstance(self, Installation):
            return "Installation"

    def resolve_authors(self, info):
        # Récupérer les auteurs liés à cette Performance
        return self.authors.all()

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Artwork)

    @convert_django_field.register(TaggableManager)
    def convert_field_to_string(field, registry=None):
        return graphene.List(graphene.String, source='get_tags')


class FilmType(ArtworkType):
    class Meta:
        model = Film
        interfaces = (graphene.relay.Node,)


class InstallationType(ArtworkType):
    class Meta:
        model = Installation
        interfaces = (graphene.relay.Node,)


class PerformanceType(ArtworkType):
    class Meta:
        model = Performance
        interfaces = (graphene.relay.Node,)


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class Query(graphene.ObjectType):

    production = graphene.Field(ProductionType, id=graphene.Int())
    productions = graphene.List(
        ProductionType, titleStartsWith=graphene.String())

    artwork = graphene.Field(ArtworkType, id=graphene.Int())
    artworks = graphene.List(ArtworkType)

    film = graphene.Field(FilmType, id=graphene.Int())
    films = graphene.List(FilmType)

    installation = graphene.Field(InstallationType, id=graphene.Int())
    installations = graphene.List(InstallationType)

    performance = graphene.Field(PerformanceType, id=graphene.Int())
    performances = graphene.List(PerformanceType)

    event = graphene.Field(EventType, id=graphene.Int())
    events = graphene.List(EventType)

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
        return Artwork.objects.all()

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

    # Task
    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_task(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Task.objects.get(pk=id)
        return None
