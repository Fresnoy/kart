from rest_framework import viewsets, permissions

from .models import Place, Award, Reward

from .serializers import PlaceSerializer, AwardSerializer, RewardSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
