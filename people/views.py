from django.contrib.auth.tokens import default_token_generator
from django.utils.http import base36_to_int
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .permissions import IsStaffOrTargetUser
from .models import Artist, User, FresnoyProfile, Staff, Organization
from .serializers import (
    ArtistSerializer, UserSerializer, FresnoyProfileSerializer,
    StaffSerializer, OrganizationSerializer
)
from common.utils import send_activation_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            profile_data = request.data.pop('profile')
            user = User.objects.create(**request.data)
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            # set user in profile
            profile_data['user'] = user
            # save profile
            FresnoyProfile.objects.create(**profile_data)
            if(request.user.is_anonymous()):
                send_activation_email(user, password)

            return Response(serializer.validated_data)

        else:
            return Response(serializer.errors)

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


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


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
