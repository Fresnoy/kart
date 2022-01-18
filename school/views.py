from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.http import base36_to_int

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_jwt.settings import api_settings

from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet

from rest_auth.views import PasswordResetView

from guardian.shortcuts import assign_perm

from people.models import User, FresnoyProfile, Artist
from people.serializers import UserRegisterSerializer

from .models import Promotion, Student, StudentApplication, StudentApplicationSetup
from .serializers import (StudentPasswordResetSerializer,
                          PromotionSerializer, StudentSerializer,
                          StudentAutocompleteSerializer,
                          PublicStudentApplicationSerializer, StudentApplicationSerializer,
                          StudentApplicationSetupSerializer
                          )

from .utils import (
                    send_activation_email,
                    send_account_information_email,
                    send_candidature_completed_email_to_user,
                    send_candidature_completed_email_to_admin,
                    send_candidature_complete_email_to_candidat,
                    send_interview_selection_email_to_candidat,
                    send_interview_selection_on_waitlist_email_to_candidat,
                    send_selected_candidature_email_to_candidat,
                    send_selected_on_waitlist_candidature_email_to_candidat,
                    send_not_selected_candidature_email_to_candidat,
                    candidature_close,
                    )


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('user__username',)
    ordering_fields = ('user__last_name',)
    filterset_fields = ('artist',
                        'user',
                        'promotion',)


class StudentAutocompleteSearchViewSet(HaystackViewSet):
    index_models = [Student]
    serializer_class = StudentAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StudentApplicationSetupViewSet(viewsets.ModelViewSet):
    # queryset = StudentApplicationSetup.objects.filter(is_current_setup=True)
    queryset = StudentApplicationSetup.objects.all()
    serializer_class = StudentApplicationSetupSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_current_setup',)


class StudentApplicationViewSet(viewsets.ModelViewSet):
    queryset = StudentApplication.objects.all()
    # serializer_class = StudentApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('=artist__user__username', 'artist__user__last_name')
    filterset_fields = ('application_completed',
                        'application_complete',
                        'selected_for_interview', 'remote_interview', 'wait_listed_for_interview',
                        'selected', 'unselected',
                        'campaign__is_current_setup',
                        'wait_listed',)
    ordering_fields = ('id',
                       'artist__user__last_name',
                       'artist__user__profile__nationality',
                       'position_in_interview_waitlist',
                       'position_in_waitlist',)

    def get_serializer_class(self, *args, **kwargs):
        """
        This switch serializers
        From Staff (and StudentApplication owner) to private and Other to public
        """
        if (self.request.user.is_authenticated and
            (self.request.user.is_staff or
             StudentApplication.objects.filter(artist__user=self.request.user.id))):
            return StudentApplicationSerializer
        return PublicStudentApplicationSerializer

    def get_queryset(self):
        """
        This query give all Application'user
        for Staff Anonymous User and gave all application for the others
        """
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            return StudentApplication.objects.filter(artist__user=user.id)
        else:
            return StudentApplication.objects.all()

    def create(self, request):
        """
        This view create an application AND Artist for auth user
        """
        user = self.request.user
        # first of all test current campaign
        if candidature_close() and not user.is_staff:
            errors = {'candidature': 'expired'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)
        campaign = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
        # user muse be auth
        if user.is_authenticated:
            # is an current inscription
            current_year_application = StudentApplication.objects.filter(
                artist__user=user.id,
                campaign=campaign
            )
            if not current_year_application:
                # take the artist
                user_artist = Artist.objects.filter(user=user.id)
                if not user_artist:
                    # if not, create it
                    user_artist = Artist(user=user)
                    user_artist.save()
                else:
                    # take the first one
                    user_artist = user_artist[0]
                # get previous apps
                last_applications = StudentApplication.objects.filter(artist__user=user.id) \
                                                              .values_list('created_on__year', flat=True)
                # transform all user previous app to string : "2001, 2002, xxxx"
                last_applications_years = ", ".join(map(str, list(last_applications)))
                # set application params
                student_application = StudentApplication(artist=user_artist, campaign=campaign,
                                                         first_time=not last_applications.exists(),
                                                         last_applications_years=last_applications_years
                                                         )
                # create application
                student_application.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                # user can't create two application for this year
                errors = {'candidature': 'you are not able to create another candidature this session'}
                return Response(errors, status=status.HTTP_409_CONFLICT)
        else:
            # FIXME: dead code: handled by APIView.permission_denied which raise HTTP_403
            errors = {'candidature': 'forbidden'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        """
        This view update an application before expiration date - staff can pass through
        """
        user = self.request.user
        # Must update one info at once
        if len(request.data) > 1 and not user.is_staff:
            errors = {'Error': 'Must update one info at once'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)
        # candidate can't update candidature when she's expired, admin can !
        if candidature_close() and not user.is_staff:
            errors = {'candidature': 'expired'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)
        # Only admin user can update selection's fields
        if (
            not user.is_staff and (
                request.data.get('application_complete') or
                request.data.get('selected_for_interview') or
                request.data.get('selected') or
                request.data.get('unselected') or
                request.data.get('wait_listed') or
                request.data.get('wait_listed_for_interview') or
                request.data.get('position_in_waitlist') or
                request.data.get('position_in_interview_waitlist') or
                request.data.get('application_complete') or  # FIXME: complete or completed?
                request.data.get('campaign'))
        ):
            errors = {'Error': 'Field permission denied'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)

        # FIXME: dead code since it never pass througth the previous test
        # send email to admin and USER (who click) is completed
        if(request.data.get('application_completed')):
            application = self.get_object()
            send_candidature_completed_email_to_user(request, user, application)
            send_candidature_completed_email_to_admin(request, user, application)

        # send email to candidat when candidature is complete (admin valid infos)
        if(request.data.get('application_complete')):
            application = self.get_object()
            candidat = application.artist.user
            send_candidature_complete_email_to_candidat(request, candidat, application)

        # send email to candidat when on interview waiting list
        if(request.data.get('wait_listed_for_interview')):
            application = self.get_object()
            candidat = application.artist.user
            send_interview_selection_on_waitlist_email_to_candidat(request, candidat, application)

        # send email to candidat when select for interviews
        if(request.data.get('selected_for_interview')):
            application = self.get_object()
            candidat = application.artist.user
            send_interview_selection_email_to_candidat(request, candidat, application)

        # send email to candidat when selected
        if(request.data.get('selected')):
            application = self.get_object()
            candidat = application.artist.user
            send_selected_candidature_email_to_candidat(request, candidat, application)

        # send email to candidat when is select on waiting list
        if(request.data.get('wait_listed')):
            application = self.get_object()
            candidat = application.artist.user
            send_selected_on_waitlist_candidature_email_to_candidat(request, candidat, application)

        # send email to candidat when is not selected
        if(request.data.get('unselected')):
            application = self.get_object()
            candidat = application.artist.user
            send_not_selected_candidature_email_to_candidat(request, candidat, application)

        # basic update
        return super(self.__class__, self).update(request, *args, **kwargs)

    @action(methods=['POST'], permission_classes=[permissions.AllowAny], detail=False)
    def user_register(self, request):
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
            # FIXME: adding a work proof to avoid dumb spambots
            send_activation_email(request, user)

            return Response(user.id, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['POST'], permission_classes=[permissions.AllowAny], detail=False)
    def user_resend_activation_email(self, request):
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


def user_activate(request, uidb64, token):
    """
    Check activation token for newly registered users. If successful,
    mark as active and log them in. If not, show an error page
    """
    # Look up the user object
    uid_int = base36_to_int(uidb64)
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
            # FIXME: if activation is already_ok the previous branch is taken
            # activation already ok
            activation_already_ok = render_to_string('emails/account/activation_already_ok.html', {
                                                     'username': user.username,
                                                     'email': user.email,
                                                     'link_change_password': change_password_link})
            return HttpResponse(activation_already_ok)

    # pas le bon token
    activation_error_page = render_to_string('emails/account/activation_error.html', {'id': uid_int})
    return HttpResponse(activation_error_page)


class UserPasswordResetView(PasswordResetView):
    serializer_class = StudentPasswordResetSerializer
