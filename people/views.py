from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import (
    Artist, User, FresnoyProfile, Staff, Organization
)
from .serializers import (
    ArtistSerializer, UserSerializer, PublicUserSerializer,
    FresnoyProfileSerializer, StaffSerializer,
    OrganizationSerializer
)


# django-guardian anonymous user
try:
    ANONYMOUS_USER_NAME = settings.ANONYMOUS_USER_NAME
except AttributeError:
    ANONYMOUS_USER_NAME = "AnonymousUser"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(username=ANONYMOUS_USER_NAME)
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
            # FIXME: dead code: afaik msg.send() will except on errors
            return Response({'error': 'Email(s) not sent'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        errors = {'error': "User : {} can't send email".format(user)}
        return Response(errors, status=status.HTTP_401_UNAUTHORIZED)

    # FIXME: dead code: handled by APIView.permission_denied which raise HTTP_403
    errors = {'error': "Not Authenticated"}
    return Response(errors, status=status.HTTP_401_UNAUTHORIZED)


class FresnoyProfileViewSet(viewsets.ModelViewSet):
    queryset = FresnoyProfile.objects.all()
    serializer_class = FresnoyProfileSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username',)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username',)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
