from django.db.models import Prefetch

from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (Artwork, Film, Installation, Performance,
                     FilmGenre, InstallationGenre, Event,
                     Itinerary, ProductionStaffTask, ProductionOrganizationTask,
                     OrganizationTask)

from .serializers import (ArtworkPolymorphicSerializer, FilmSerializer, InstallationSerializer, KeywordsSerializer,
                          PerformanceSerializer, FilmGenreSerializer,
                          InstallationGenreSerializer, EventSerializer,
                          ItinerarySerializer, ProductionStaffTaskSerializer,
                          PartnerSerializer, OrganizationTaskSerializer
                          )


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkPolymorphicSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


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
