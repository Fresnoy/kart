from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset, password_reset_confirm

from django.utils.http import base36_to_int
from django.http import HttpResponse
from django.template.loader import render_to_string

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from guardian.shortcuts import assign_perm

from .models import Artist, User, FresnoyProfile, Staff, Organization
from .serializers import (
    ArtistSerializer, UserSerializer, UserRegisterSerializer,
    FresnoyProfileSerializer, StaffSerializer,
    OrganizationSerializer
)
from .utils import send_activation_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # save user
            user = User(first_name=request.data.get('first_name'),
                        last_name=request.data.get('last_name'),
                        username=request.data.get('username'),
                        email=request.data.get('email'))
            user.is_active = False
            user.save()
            profile = FresnoyProfile.objects.create(user=user)
            # assign permission
            assign_perm('change_user', user, user)
            assign_perm('change_fresnoyprofile', user, profile)
            # assign group
            group = Group.objects.get(name='School Application')
            user.groups.add(group)
            send_activation_email(request, user)
            return Response({'user': True}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors)

    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
        except User.DoesNotExist:
            return Response({'user': False}, status=status.HTTP_204_NO_CONTENT)

        return Response({'user': reverse('user-detail', kwargs={'pk': user.id})}, status=status.HTTP_200_OK)


def activate(request, uidb36, token):
    """
    Check activation token for newly registered users. If successful,
    mark as active and log them in. If not, show an error page
    """
    # Look up the user object
    uid_int = base36_to_int(uidb36)

    try:
        user = User.objects.get(pk=uid_int)
    except User.DoesNotExist:
        user = None

    if user is not None:

        change_password_link = reverse('password-reset')
        # Is the token valid?
        if default_token_generator.check_token(user, token):
            # Activate the user
            user.is_active = True
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            activation_ok_show_password_page = render_to_string('account/activation_ok_show_password.html', {
                                                                'id': uid_int,
                                                                'password': password,
                                                                'link_change_password': change_password_link})
            return HttpResponse(activation_ok_show_password_page)
        else:
            # activation deja faite
            activation_already_ok = render_to_string('account/activation_already_ok.html', {
                                                     'username': user.username,
                                                     'email': user.email,
                                                     'link_change_password': change_password_link})
            return HttpResponse(activation_already_ok)

    # pas le bon token
    activation_error_page = render_to_string('account/activation_error.html', {'id': uid_int})
    return HttpResponse(activation_error_page)


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request,
                                  template_name='account/password_reset_confirm.html',
                                  uidb64=uidb64,
                                  token=token,
                                  post_reset_redirect=reverse('admin:login'))


def reset(request):
    return password_reset(request,
                          template_name='account/password_reset_form.html',
                          email_template_name='emails/password_reset_email.html',
                          subject_template_name='emails/password_reset_subject.txt',
                          post_reset_redirect=reverse('admin:login'))


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
