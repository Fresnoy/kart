from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response

from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet

from people.models import Artist

from .models import Promotion, Student, StudentApplication, StudentApplicationSetup
from .serializers import (PromotionSerializer, StudentSerializer,
                          StudentAutocompleteSerializer,
                          PublicStudentApplicationSerializer, StudentApplicationSerializer,
                          StudentApplicationSetupSerializer
                          )

from .utils import (send_candidature_completed_email_to_user,
                    send_candidature_completed_email_to_admin,
                    send_candidature_complete_email_to_candidat,
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
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('user__username',)
    ordering_fields = ('user__last_name',)
    filter_fields = ('artist',
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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('is_current_setup',)


class StudentApplicationViewSet(viewsets.ModelViewSet):
    queryset = StudentApplication.objects.all()
    # serializer_class = StudentApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('=artist__user__username',)
    filter_fields = ('application_completed',
                     'application_complete',
                     'selected_for_interview', 'remote_interview', 'wait_listed_for_interview',
                     'selected', 'unselected',
                     'campain__is_current_setup',
                     'wait_listed',)
    ordering_fields = ('id',
                       'artist__user__last_name',
                       'artist__user__profile__nationality',)

    def get_serializer_class(self, *args, **kwargs):
        """
        This switch serializers
        From Staff (and StudentApplication owner) to private and Other to public
        """
        if (
            self.request.user.is_staff or
            StudentApplication.objects.filter(artist__user=self.request.user.id)
           ):
            return StudentApplicationSerializer
        return PublicStudentApplicationSerializer

    def get_queryset(self):
        """
        This query give all Application'user
        for Staff Anonymous User and gave all application for the others
        """
        user = self.request.user
        if user.is_authenticated() and not user.is_staff:
            return StudentApplication.objects.filter(artist__user=user.id)
        else:
            return StudentApplication.objects.all()

    def create(self, request):
        """
        This view create an application AND Artist for auth user
        """
        user = self.request.user
        # first of all test current campain
        if candidature_close() and not user.is_staff:
            errors = {'candidature': 'expired'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)
        campain = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
        # user muse be auth
        if user.is_authenticated():
            # is an current inscription
            current_year_application = StudentApplication.objects.filter(
                artist__user=user.id,
                campain=campain
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
                # create application
                student_application = StudentApplication(artist=user_artist, campain=campain)
                student_application.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                # user can't create two application for this year
                errors = {'candidature': 'you are not able to create another candidature this session'}
                return Response(errors, status=status.HTTP_409_CONFLICT)
        else:
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
                request.data.get('wait_listed') or
                request.data.get('application_complete') or
                request.data.get('campain'))
        ):
            errors = {'Error': 'Field permission denied'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)

        # send email when candidature to admin and USER (who click) is completed
        if(request.data.get('application_completed')):
            application = self.get_object()
            send_candidature_completed_email_to_user(request, user, application)
            send_candidature_completed_email_to_admin(request, user, application)

        # send email when to candidat when candidature is complete
        if(request.data.get('application_complete')):
            application = self.get_object()
            candidat = application.artist.user
            send_candidature_complete_email_to_candidat(request, candidat, application)
        # basic update
        return super(self.__class__, self).update(request, *args, **kwargs)
