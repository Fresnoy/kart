# -*- coding: utf-8 -*-
from django.urls import re_path

from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseBadRequest


from haystack.query import SearchQuerySet
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash

from common.api import WebsiteResource, BTBeaconResource
from assets.api import GalleryResource
from people.api import ArtistResource, OrganizationResource, StaffResource
from diffusion.api import PlaceResource

from .models import Installation, Film, Performance, Event, Itinerary, Artwork
from .models import ProductionOrganizationTask, OrganizationTask
from .models import FilmGenre, StaffTask, ProductionStaffTask


class StaffTaskResource(ModelResource):
    class Meta:
        queryset = StaffTask.objects.all()
        resource_name = "production/stafftask"


class ProductionStaffTaskResource(ModelResource):
    class Meta:
        queryset = ProductionStaffTask.objects.all()
        resource_name = "production/productionstafftask"

    staff = fields.ForeignKey(StaffResource, 'staff', full=True)
    task = fields.ForeignKey(StaffTaskResource, 'task', full=True)


class OrganizationTaskResource(ModelResource):
    class Meta:
        queryset = OrganizationTask.objects.all()
        resource_name = "production/organisationtask"


class ProductionOrganizationTaskResource(ModelResource):
    class Meta:
        queryset = ProductionOrganizationTask.objects.all()
        resource_name = "production/productionorganizationtask"

    organization = fields.ForeignKey(OrganizationResource, 'organization', full=True)
    task = fields.ForeignKey(StaffTaskResource, 'task', full=True)


class ProductionResource(ModelResource):
    collaborators = fields.ToManyField(ProductionStaffTaskResource, 'staff_tasks', full=True)
    partners = fields.ToManyField(ProductionOrganizationTaskResource, 'organization_tasks', full=True)
    websites = fields.ToManyField(WebsiteResource, 'websites', full=True)


class AbstractArtworkResource(ProductionResource):
    """
    A model shared by Artwork subclasses, required to prevent
    dehydrate from looping because of ArtworkResource being shared
    """
    process_galleries = fields.ToManyField(GalleryResource, 'process_galleries', full=True)
    mediation_galleries = fields.ToManyField(GalleryResource, 'mediation_galleries', full=True)
    in_situ_galleries = fields.ToManyField(GalleryResource, 'in_situ_galleries', full=True)
    press_galleries = fields.ToManyField(GalleryResource, 'press_galleries', full=True)
    teaser_galleries = fields.ToManyField(GalleryResource, 'teaser_galleries', full=True)

    authors = fields.ToManyField(ArtistResource, 'authors')
    beacons = fields.ToManyField(BTBeaconResource, 'beacons', full=True)

    def dehydrate(self, bundle):
        bundle.data["type"] = '{0}'.format(self.Meta.queryset.model.__name__.lower())

        return bundle


class ArtworkResource(AbstractArtworkResource):
    class Meta:
        queryset = Artwork.objects.all()
        resource_name = 'production/artwork'
        filtering = {
            'authors': ALL_WITH_RELATIONS,
            'events': ALL_WITH_RELATIONS,
            'title': ALL,
            'genres': ALL_WITH_RELATIONS
        }
        # cache = SimpleCache(timeout=10)

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)
    events = fields.ToManyField('production.api.EventResource', 'events', null=True, blank=True, full=False)
    award = fields.ToManyField('diffusion.api.AwardResource', 'award', blank=True, full=False)

    def dehydrate(self, bundle):
        res_types = (InstallationResource, FilmResource, PerformanceResource)

        for res_type in res_types:
            if isinstance(bundle.obj, res_type.Meta.queryset.model):
                res = res_type()
                rr_bundle = res.build_bundle(obj=bundle.obj, request=bundle.request)
                bundle.data = res.full_dehydrate(rr_bundle).data
                bundle.data['type'] = u"{0}".format(res_type.Meta.queryset.model.__name__.lower())
                break

        return bundle

    def prepend_urls(self):
        return [
            # path(f"<str:resource_name>{self._meta.resource_name})/search{trailing_slash()}",
            re_path(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('get_search'),
                    name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Film,
                                      Installation,
                                      Performance).load_all().autocomplete(content_auto=request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except ValueError:
            return HttpResponseBadRequest("Bad page number.")
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)


class InstallationGenreResource(ModelResource):
    class Meta:
        queryset = FilmGenre.objects.all()
        resource_name = 'production/installationgenre'


class InstallationResource(AbstractArtworkResource):
    class Meta:
        queryset = Installation.objects.all()
        resource_name = 'production/installation'
        filtering = {'authors': ALL_WITH_RELATIONS, 'events': ALL_WITH_RELATIONS}

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)
    events = fields.ToManyField('production.api.EventResource', 'events', blank=True, full=False)
    genres = fields.ToManyField(InstallationGenreResource, 'genres', full=True)


class FilmGenreResource(ModelResource):
    class Meta:
        queryset = FilmGenre.objects.all()
        resource_name = 'production/filmgenre'


class FilmResource(AbstractArtworkResource):
    class Meta:
        queryset = Film.objects.all()
        resource_name = 'production/film'
        filtering = {'authors': ALL_WITH_RELATIONS, 'events': ALL_WITH_RELATIONS, 'genres': ALL_WITH_RELATIONS}

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)
    events = fields.ToManyField('production.api.EventResource', 'events', blank=True, full=False)
    genres = fields.ToManyField(FilmGenreResource, 'genres', full=True, full_detail=True, full_list=False)
    awards = fields.ToManyField('diffusion.api.AwardResource', 'award', blank=True, full=False)


class PerformanceResource(AbstractArtworkResource):
    class Meta:
        queryset = Performance.objects.all()
        resource_name = 'production/performance'
        filtering = {'authors': ALL_WITH_RELATIONS, 'events': ALL_WITH_RELATIONS, 'genres': ALL_WITH_RELATIONS}

    authors = fields.ToManyField(ArtistResource, 'authors', full=True, full_detail=True, full_list=False)

    events = fields.ToManyField('production.api.EventResource', 'events', blank=True, full=False)


class EventResource(ProductionResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'production/event'

    place = fields.ForeignKey(PlaceResource, 'place', full=True, null=True)

    installations = fields.ToManyField(InstallationResource, 'installations',
                                       full=True, full_list=False, full_detail=True)

    films = fields.ToManyField(FilmResource, 'films', full=True, full_list=False, full_detail=True)

    performances = fields.ToManyField(PerformanceResource, 'performances', full=True, full_list=False, full_detail=True)

    subevents = fields.ToManyField('production.api.EventResource', 'subevents', blank=True, full=False)


class ItineraryResource(ModelResource):
    class Meta:
        queryset = Itinerary.objects.all()
        resource_name = 'production/itinerary'

    artworks = fields.ToManyField(ArtworkResource, 'artworks', use_in=['detail'],
                                  full_detail=True, full_list=False, full=True, blank=True)

    gallery = fields.ToManyField(GalleryResource, 'gallery', use_in=['detail'],
                                 full_detail=True, full=True, blank=True)


class ExhibitionResource(EventResource):
    class Meta:
        queryset = Event.objects.filter(type='EXHIB')
        resource_name = 'production/exhibition'

    itineraries = fields.ToManyField(ItineraryResource, 'itineraries', full_list=False, full_detail=True)
