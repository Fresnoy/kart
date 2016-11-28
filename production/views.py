from rest_framework import viewsets

from .models import (Film, Installation, Performance,
                     FilmGenre, InstallationGenre, Event,
                     Itinerary)

from .serializers import (FilmSerializer, InstallationSerializer,
                          PerformanceSerializer, FilmGenreSerializer,
                          InstallationGenreSerializer, EventSerializer,
                          ItinerarySerializer)


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class InstallationViewSet(viewsets.ModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ItineraryViewSet(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer


class FilmGenreViewSet(viewsets.ModelViewSet):
    queryset = FilmGenre.objects.all()
    serializer_class = FilmGenreSerializer


class InstallationGenreViewSet(viewsets.ModelViewSet):
    queryset = InstallationGenre.objects.all()
    serializer_class = InstallationGenreSerializer
