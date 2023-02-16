from django.db.models import Prefetch

from rest_framework import viewsets, permissions, pagination
from rest_framework.response import Response

from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (Artwork, Film, Installation, Performance,
                     FilmGenre, InstallationGenre, Event,
                     Itinerary, ProductionStaffTask, ProductionOrganizationTask,
                     OrganizationTask)

from .serializers import (ArtworkPolymorphicSerializer, ArtworkAutocompleteSerializer,
                          FilmSerializer, InstallationSerializer, KeywordsSerializer,
                          PerformanceSerializer, FilmGenreSerializer,
                          InstallationGenreSerializer, EventSerializer,
                          ItinerarySerializer, ProductionStaffTaskSerializer,
                          PartnerSerializer, OrganizationTaskSerializer
                          )


class CustomPagination(pagination.PageNumberPagination):
    """
    Customize Pagination
    """
    # no limit when page_size not set
    page_size = 100000
    page_size_query_param = 'page_size'
    max_page_size = 20
    page_query_param = 'page'

    def get_paginated_response(self, data):
        response = Response(data)
        # pagination on headers
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        return response


class ArtworkFilterSet(filters.FilterSet):
    """
    Customize Filters for Artwork
    """
    # transform date to year
    production_year = filters.NumberFilter(field_name="production_date", lookup_expr='year__exact')

    class Meta:
        model = Artwork
        fields = {
            "authors",
            "production_date",
        }


class ArtworkViewSet(viewsets.ModelViewSet,):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkPolymorphicSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArtworkFilterSet
    pagination_class = CustomPagination


class TagsFilter(filters.CharFilter):

    def filter(self, qs, value):
        if value:
            lookup_field = self.field_name + "__name__in"
            tags = [tag.strip() for tag in value.split(',')]
            qs = qs.filter(**{lookup_field: tags}).distinct()

        return qs


class ArtworkFilter(filters.FilterSet):
    keywords = TagsFilter(field_name="keywords")

    class Meta:
        model = Film
        fields = ['genres', 'keywords']


class ArtworkAutocompleteSearchViewSet(HaystackViewSet):
    index_models = [Film, Installation]
    serializer_class = ArtworkAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArtworkFilter


class InstallationViewSet(viewsets.ModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    search_fields = ('genres',)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('installations__authors', 'films__authors', 'performances__authors',)


class ItineraryViewSet(viewsets.ModelViewSet):
    #  the order of artworks in itinerary must be certain
    queryset = Itinerary.objects.all().prefetch_related(
                    Prefetch('artworks', queryset=Artwork.objects.all().order_by('itineraryartwork__order')))
    serializer_class = ItinerarySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('event',)


class FilmGenreViewSet(viewsets.ModelViewSet):
    queryset = FilmGenre.objects.all()
    serializer_class = FilmGenreSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class InstallationGenreViewSet(viewsets.ModelViewSet):
    queryset = InstallationGenre.objects.all()
    serializer_class = InstallationGenreSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class CollaboratorViewSet(viewsets.ModelViewSet):
    queryset = ProductionStaffTask.objects.all()
    serializer_class = ProductionStaffTaskSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrganizationTask.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class OrganizationTaskViewSet(viewsets.ModelViewSet):
    queryset = OrganizationTask.objects.all()
    serializer_class = OrganizationTaskSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class FilmKeywordsViewSet(viewsets.ModelViewSet):
    queryset = Film.keywords.all()
    serializer_class = KeywordsSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
