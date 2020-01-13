from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMultiAlternatives

from django.utils.http import base36_to_int
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from rest_framework_jwt.settings import api_settings

from guardian.shortcuts import assign_perm

from school.models import StudentApplicationSetup

from .models import (
    Artist, User, FresnoyProfile, Staff, Organization
)
from .serializers import (
    ArtistSerializer, UserSerializer, PublicUserSerializer, UserRegisterSerializer,
    FresnoyProfileSerializer, StaffSerializer,
    OrganizationSerializer
)
from .utils import send_activation_email, send_account_information_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username', '=email')

    def get_serializer_class(self, *args, **kwargs):
        if (
            self.request.user.is_staff or
            self.kwargs and self.request.user.pk == int(self.kwargs['pk'])
           ):
            return UserSerializer
        return PublicUserSerializer

    @action(methods=['POST'], permission_classes=[permissions.AllowAny], detail=False)
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
            # send activation email
            send_activation_email(request, user)

            return Response(user.id, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['POST'], permission_classes=[permissions.AllowAny], detail=False)
    def resend_activation_email(self, request):
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = User.objects.get(username=request.data.get('username'))
            if not user.is_active:
                user.email = request.data.get('email')
                user.save()
                send_activation_email(request, user)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                errors = {'user': ['user is active']}
                return Response(errors, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


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

        setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        custom_infos = user

        payload = jwt_payload_handler(custom_infos)
        front_token = jwt_encode_handler(payload)
        route = "candidature.account.login"

        change_password_link = "{0}/{1}/{2}".format(setup.reset_password_url, front_token, route)

        # Is the token valid?
        if default_token_generator.check_token(user, token):
            # Activate the user
            user.is_active = True
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

            send_account_information_email(user)

            return HttpResponseRedirect(change_password_link)

        else:
            # activation already ok
            activation_already_ok = render_to_string('account/activation_already_ok.html', {
                                                     'username': user.username,
                                                     'email': user.email,
                                                     'link_change_password': change_password_link})
            return HttpResponse(activation_already_ok)

    # pas le bon token
    activation_error_page = render_to_string('account/activation_error.html', {'id': uid_int})
    return HttpResponse(activation_error_page)


def verif_user_by_property(array, property):
    for item in array:
        if not User.objects.filter(**{property: item}).exists():
            return item
    return True


@api_view(['GET', 'POST', ])
@permission_classes((permissions.IsAuthenticated,))
def send_custom_emails(request, format=None):
    """
        Send emails with custom params :
            from, to, bcc, subject, message
    """
    user = request.user
    if(user.is_staff):
        items_need_list = ('from', 'to', 'bcc', 'subject', 'message',)
        verify_email = ('from', 'to', 'bcc',)
        email = {}
        if not request.POST:
            return Response({'error': 'Empty POST values'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # get values
        for item in items_need_list:
            if not request.POST.get(item):
                errors = {'error': "[{}:] var not found".format(item.upper())}
                return Response(errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            # set item
            email[item] = request.POST.get(item)
        # validation emails
        for item in verify_email:
            email[item] = email[item].split(";")
            email_in_db = verif_user_by_property(email[item], 'email')
            if email_in_db is not True:
                errors = {'error': '{} e-mail {} inconnu du system'.format(item, email_in_db)}
                return Response(errors, status=status.HTTP_403_FORBIDDEN)
        # transform messages with templates
        email['message_html'] = "<br />".join(email['message'].split("\n"))
        msg_plain = render_to_string('emails/send_custom_email.txt', {'message': email['message']})
        msg_html = render_to_string('emails/send_custom_email.html', {'message': email['message_html']})
        # create email
        msg = EmailMultiAlternatives(
            email['subject'],
            msg_plain,
            email['from'],
            email['to'],
            email['bcc'],
        )
        msg.attach_alternative(msg_html, "text/html")
        if msg.send() == 1:
            return Response({"Sent email(s)"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email(s) not sent'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        errors = {'error': "User : {} can't send email".format(user)}
        return Response(errors, status=status.HTTP_401_UNAUTHORIZED)

    errors = {'error': "Not Authenticated"}
    return Response(errors, status=status.HTTP_401_UNAUTHORIZED)


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
