from rest_framework import viewsets, permissions

from .models import Place, Award, MetaAward

from .serializers import PlaceSerializer, AwardSerializer, MetaAwardSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MetaAwardViewSet(viewsets.ModelViewSet):
    queryset = MetaAward.objects.all()
    serializer_class = MetaAwardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
