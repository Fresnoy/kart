import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field

from django.db.models import Q

from taggit.managers import TaggableManager
from taggit.models import Tag
from itertools import chain

from .models import Production, Artwork, Film, Installation, \
    Performance, Event, Task, ProductionOrganizationTask, StaffTask, ProductionStaffTask

from people.schema import ArtistType
from assets.schema import GalleryType
from common.schema import WebsiteType

from diffusion.models import Diffusion
from diffusion.schema import DiffusionType, PlaceType


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class StaffTaskType(TaskType):
    class Meta:
        model = StaffTask


class ProductionStaffTaskType(TaskType):
    class Meta:
        model = ProductionStaffTask

    staff_name = graphene.String()
    task_name = graphene.String()

    def resolve_staff_name(parent, info):
        # return artist name if any
        if parent.staff.user.artist_set.all():
            return parent.staff.user.artist_set.first()
        # else return staff name
        return parent.staff

    def resolve_task_name(parent, info):
        return parent.task


class PartnerType(DjangoObjectType):
    class Meta:
        model = ProductionOrganizationTask
    name = graphene.String()
    task_name = graphene.String()
    tasks = graphene.Field(TaskType)

    def resolve_name(parent, info):
        return parent.organization.name

    def resolve_tasks(parent, info):
        return TaskType(label=parent.task.label, description=parent.task.description)

    def resolve_task_name(parent, info):
        return parent.task.label


class ProductionInterface(graphene.Interface):
    id = graphene.ID(required=True, source='pk')
    title = graphene.String()
    former_title = graphene.String()
    subtitle = graphene.String()
    updated_on = graphene.Date()
    picture = graphene.String()
    websites = graphene.List(WebsiteType)
    collaborators = graphene.List(ProductionStaffTaskType)
    description_short_fr = graphene.String()
    description_short_en = graphene.String()
    description_fr = graphene.String()
    description_en = graphene.String()
    partners = graphene.List(PartnerType)
    production_date = graphene.Date()

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Event):
            return EventType
        if isinstance(instance, Artwork):
            return ArtworkType
        else:
            return None  #

    def resolve_partners(parent, info, **kwargs):
        pots = ProductionOrganizationTask.objects.all().filter(production=parent)
        return pots

    def resolve_collaborators(parent, info, **kwargs):
        pots = ProductionStaffTask.objects.all().filter(production=parent)
        return pots


class ArtworkInterface(ProductionInterface):
    id = graphene.ID(required=True)

    # @classmethod
    # def is_type_of(cls, root, info):
    #     return isinstance(root, Artwork)
    authors = graphene.List(ArtistType)
    diffusions = graphene.List(DiffusionType)
    mentoring = graphene.List("school.schema.TeachingArtistType")
    keywords = graphene.List("production.schema.KeywordType")

    # The type of artwork (Film, Performance, ...)
    type = graphene.String()

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Film):
            return FilmType
        if isinstance(instance, Performance):
            return PerformanceType
        if isinstance(instance, Installation):
            return InstallationType
        else:
            return None

    def resolve_mentoring(parent, info, **kwargs):
        return parent.mentoring.all()


class ProductionType(DjangoObjectType):
    class Meta:
        model = Production
        interfaces = (ProductionInterface,)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Production)


class KeywordType(DjangoObjectType):
    class Meta:
        model = Tag
    name = graphene.String()
    slug = graphene.String()


class ArtworkType(ProductionType):
    class Meta:
        model = Artwork
        interfaces = (graphene.relay.Node, ProductionInterface)

    authors = graphene.List(ArtistType)

    keywords = graphene.List(KeywordType)

    # The type of artwork (Film, Performance, ...)
    type = graphene.String()

    # Galleries
    def resolve_gallery(parent, info, galType=None):
        if galType == "process":
            return parent.process_galleries.all()
        if galType == "mediation":
            return parent.mediation_galleries.all()
        if galType == "insitu":
            return parent.in_situ_galleries.all()
        if galType == "press":
            return parent.press_galleries.all()
        if galType == "teaser":
            return parent.teaser_galleries.all()
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
    def resolve_type(parent, info):
        if isinstance(parent, Film):
            return "Film"
        if isinstance(parent, Performance):
            return "Performance"
        if isinstance(parent, Installation):
            return "Installation"

    def resolve_authors(parent, info):
        return parent.authors.all()

    def resolve_keywords(parent, info):
        return parent.keywords.all()

    def resolve_diffusions(parent, info):
        return Diffusion.objects.all().filter(artwork=parent)

    # Artworks by the same authors
    relArtworks = graphene.List(graphene.Int, aw_context=graphene.String())

    def resolve_relArtworks(parent, info, aw_context="authors", **kwargs):
        ''' Related Artworks are artworks from same author'''
        if aw_context:
            if aw_context == "authors":
                auth = parent.authors.all()
                aws = Artwork.objects.all().filter(authors__in=auth)
                return [aw.id for aw in aws if aw.id != parent.id]
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


def order(aws, orderby):
    # Sort the artworks
    def tt(x):
        # if orderby == "author":
        #     art = x.authors.all().order_by('user__last_name').first().user.last_name
        if orderby == "author":
            first_auth = x.authors.first()
            # default
            art = first_auth.__str__()
            # default if not collective
            if first_auth.user is not None:
                art = first_auth.user.last_name
            # alpha order or nickname
            if first_auth.alphabetical_order != "":
                art = first_auth.alphabetical_order
            elif first_auth.nickname != "":
                art = first_auth.nickname
        elif orderby == "title":
            art = x.title
        elif orderby == "id":
            art = x.id
        else:
            raise Exception("orderby value is undefined or unknown")
        return (art)

    return sorted(aws, key=lambda x: tt(x))


class ArtworkEventType(graphene.ObjectType):
    artwork = graphene.Field(ArtworkType)
    next_alpha = graphene.Field(ArtworkType)
    prev_alpha = graphene.Field(ArtworkType)
    next_author = graphene.Field(ArtworkType)
    prev_author = graphene.Field(ArtworkType)


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        interfaces = (ProductionInterface,)

    artworks = graphene.List(
        ArtworkType, orderby=graphene.String(default_value="author"))
    # artwork = graphene.Field(ArtworkType, id=graphene.ID())
    artworkExhib = graphene.Field(ArtworkEventType, id=graphene.ID())

    place = graphene.Field(PlaceType)

    def resolve_artworkExhib(parent, info, **kwargs):
        id = kwargs.get('id')

        aws = list(chain(parent.installations.all(),
                         parent.films.all(), parent.performances.all()))

        if id is not None:
            aw = Artwork.objects.get(pk=id)
            if aw not in aws:
                raise Exception(
                    "The artwork is not programmed in the current event")

            awsByAlpha = order(aws, "title")
            awsByAuthor = order(aws, "author")

            ind = awsByAlpha.index(aw)+1
            #  if out of maximmum bound, restart from 1st index
            if ind == len(awsByAlpha):
                ind = 0
            next_alpha = awsByAlpha[ind]

            ind = awsByAlpha.index(aw)-1
            if ind < -len(awsByAlpha):
                # if out of minium bound, restart from last index
                ind = len(awsByAlpha) - 1
            prev_alpha = awsByAlpha[ind]

            ind = awsByAuthor.index(aw)+1
            #  if out of maximmum bound, restart from 1st index
            if ind == len(awsByAuthor):
                ind = 0
            next_author = awsByAuthor[ind]

            ind = awsByAuthor.index(aw)-1
            if ind < -len(awsByAuthor):
                # if out of minium bound, restart from last index
                ind = len(awsByAuthor) - 1
            prev_author = awsByAuthor[ind]

            return ArtworkEventType(artwork=aw, next_alpha=next_alpha, prev_alpha=prev_alpha,
                                    prev_author=prev_author, next_author=next_author)
        return None

    def resolve_artworks(parent, info, orderby=None, **kwargs):

        # Collect all artworks
        aws = list(chain(parent.installations.all(),
                   parent.films.all(), parent.performances.all()))

        if orderby:
            return order(aws, orderby)
        return aws


class ExhibitionType(EventType):
    class Meta:
        model = Event


class Query(graphene.ObjectType):

    production = graphene.Field(ProductionType, id=graphene.Int())
    productions = graphene.List(
        ProductionInterface, titleStartsWith=graphene.String())

    artwork = graphene.Field(ArtworkType, id=graphene.Int())
    artworks = graphene.List(ArtworkInterface,
                            title=graphene.String(required=False),
                            hasKeywordName=graphene.List(graphene.String, required=False),
                            belongProductionYear=graphene.String(required=False),
                            hasType=graphene.String(required=False))

    film = graphene.Field(FilmType, id=graphene.Int())
    films = graphene.List(FilmType)

    installation = graphene.Field(InstallationType, id=graphene.Int())
    installations = graphene.List(InstallationType)

    performance = graphene.Field(PerformanceType, id=graphene.Int())
    performances = graphene.List(PerformanceType)

    event = graphene.Field(EventType, id=graphene.Int())
    events = graphene.List(EventType, eventTitleContains=graphene.String(),
                           eventPlaceStartWith=graphene.String())

    exhibition = graphene.Field(ExhibitionType, id=graphene.Int())
    exhibitions = graphene.List(ExhibitionType)

    partners = graphene.Field(PartnerType, id=graphene.Int())
    partnerss = graphene.List(PartnerType)

    task = graphene.Field(TaskType, id=graphene.Int())
    tasks = graphene.List(TaskType)

    stafftask = graphene.Field(StaffTaskType, id=graphene.Int())
    stafftasks = graphene.List(StaffTaskType)

    # Production
    def resolve_productions(root, info, titleStartsWith=None, **kwargs):
        productions = Production.objects.all()

        if titleStartsWith:
            productions = productions.filter(
                title__istartswith=titleStartsWith)
            return productions
        return productions

    def resolve_production(root, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Production.objects.get(pk=id)
        return None
    

    # Artwork
    def resolve_artworks(root, info, hasKeywordName=None, belongProductionYear=None, hasType=None, **kwargs):
        title = kwargs.get('title')
        artworks = Artwork.objects.all()

        if title:
            artworks = artworks.filter(Q(title__icontains=title) |
                                          Q(former_title__icontains=title) |
                                          Q(subtitle__icontains=title))
        if hasKeywordName and hasKeywordName[0] != "":
            artworks = artworks.filter(
                keywords__name__in=hasKeywordName)
        if belongProductionYear:
            artworks = artworks.filter(
                production_date__year=belongProductionYear)
        if hasType:
            if hasType.lower() == 'film':
                artworks = artworks.filter(
                    film__isnull=False)
            elif hasType.lower() == 'performance':
                artworks = artworks.filter(
                    performance__isnull=False)
            elif hasType.lower() == 'installation':
                artworks = artworks.filter(
                    installation__isnull=False)
            else:
                # Empty response if artworks aren't one of the previous type
                artworks = artworks.filter(id__in=[])
        return artworks.order_by('authors__user__last_name').all()

    def resolve_artwork(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Artwork.objects.get(pk=id)
        return None
    
    # Film
    def resolve_films(root, info, **kwargs):
        return Film.objects.all()

    def resolve_film(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Film.objects.get(pk=id)
        return None

    # Installation
    def resolve_installations(root, info, **kwargs):
        return Installation.objects.all()

    def resolve_installation(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Installation.objects.get(pk=id)
        return None

    # Performance
    def resolve_performances(root, info, **kwargs):
        return Performance.objects.all()

    def resolve_performance(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Performance.objects.get(pk=id)
        return None

    # Event
    def resolve_events(root, info, eventTitleContains=None, eventPlaceStartWith=None, **kwargs):
        if eventTitleContains:
            return Event.objects.filter(
                title__icontains=eventTitleContains,
                )
        if eventPlaceStartWith:
            return Diffusion.objects.filter(
                place__name__istartswith=eventPlaceStartWith,
                ) | Diffusion.objects.filter(
                place__city__istartswith=eventPlaceStartWith,
                ) | Diffusion.objects.filter(
                place__country__iexact=eventPlaceStartWith,
                ) | Diffusion.objects.filter(
                place__country__iname=eventPlaceStartWith,
                )
        return Event.objects.all()

    def resolve_event(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Event.objects.get(pk=id)
        return None

    # Exhibition
    def resolve_exhibitions(root, info, **kwargs):
        return Event.objects.all()

    def resolve_exhibition(root, info, **kwargs):

        id = kwargs.get('id')
        if id is not None:
            return Event.objects.get(pk=id)
        return None

    # Task
    def resolve_tasks(root, info, **kwargs):
        return Task.objects.all()

    def resolve_task(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Task.objects.get(pk=id)
        return None

    # StaffTask
    def resolve_stafftasks(root, info, **kwargs):
        return StaffTask.objects.all()

    def resolve_stafftask(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return StaffTask.objects.get(pk=id)
        return None
