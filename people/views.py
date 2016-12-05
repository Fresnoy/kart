from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from django.utils.http import base36_to_int
from django.http import HttpResponse

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import list_route

from guardian.shortcuts import assign_perm

from .models import Artist, User, FresnoyProfile, Staff, Organization
from .serializers import (
    ArtistSerializer, UserSerializer, UserRegisterSerializer,
    FresnoyProfileSerializer, StaffSerializer,
    OrganizationSerializer
)
from common.utils import send_activation_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = User(first_name=serializer.data.get('first_name'),
                        last_name=serializer.data.get('last_name'),
                        username=serializer.data.get('username'),
                        email=serializer.data.get('email'))
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            profile = FresnoyProfile.objects.create(user=user)
            # assign permission
            assign_perm('change_user', user, user)
            assign_perm('change_fresnoyprofile', user, profile)
            # assign group
            group = Group.objects.get(name='School Application')
            user.groups.add(group)
            send_activation_email(request, user, password)
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


def activate(request, uidb36, token):
    """
    Check activation token for newly registered users. If successful,
    mark as active and log them in. If not, show an error page.
    Code borrowed from Django's auth reset mechanism.
    """
    # Look up the user object
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(pk=uid_int)
    except (ValueError, OverflowError):
        user = None

    if user is not None:

        # Is the token valid?
        if default_token_generator.check_token(user, token):

            # Activate the user
            user.is_active = True
            user.save()

            # Log in the user
            # user.backend = settings.AUTHENTICATION_BACKENDS[0]
            # auth_login(request, user)

            # Redirect to URL specified in settings
            return HttpResponse("OKVALIDE")

    return HttpResponse("Error")


class FresnoyProfileViewSet(viewsets.ModelViewSet):
    queryset = FresnoyProfile.objects.all()
    serializer_class = FresnoyProfileSerializer




class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
