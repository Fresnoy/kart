from rest_framework import viewsets

from .models import Artist, User, FresnoyProfile, Staff, Organization
from .serializers import (
    ArtistSerializer, UserSerializer, FresnoyProfileSerializer,
    StaffSerializer, OrganizationSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FresnoyProfileViewSet(viewsets.ModelViewSet):
    queryset = FresnoyProfile.objects.all()
    serializer_class = FresnoyProfileSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
