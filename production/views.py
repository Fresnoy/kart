from rest_framework import viewsets, permissions, filters

from .models import (Film, Installation, Performance,
                     FilmGenre, InstallationGenre, Event,
                     Itinerary, ProductionStaffTask, ProductionOrganizationTask,
                     OrganizationTask)

from .serializers import (FilmSerializer, InstallationSerializer,
                          PerformanceSerializer, FilmGenreSerializer,
                          InstallationGenreSerializer, EventSerializer,
                          ItinerarySerializer, ProductionStaffTaskSerializer,
                          PartnerSerializer, OrganizationTaskSerializer
                          )


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class InstallationViewSet(viewsets.ModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class ItineraryViewSet(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


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
