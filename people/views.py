from signals import create_user_with_profile

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .permissions import IsStaffOrTargetUser
from .models import Artist, User, FresnoyProfile, Staff, Organization
from .serializers import (
    ArtistSerializer, UserSerializer, FresnoyProfileSerializer,
    StaffSerializer, OrganizationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        created = super(UserViewSet, self).create(request, *args, **kwargs)

        # created
        if(request.user.is_anonymous()):
            pass

        return created

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


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
