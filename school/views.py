import datetime

from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response

from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet

from people.models import Artist

from .models import Promotion, Student, StudentApplication, StudentApplicationSetup
from .serializers import (PromotionSerializer, StudentSerializer,
                          StudentAutocompleteSerializer, StudentApplicationSerializer
                          )

from .utils import (send_candidature_completed_email_to_user,
                    send_candidature_completed_email_to_admin
                    )


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StudentAutocompleteSearchViewSet(HaystackViewSet):
    index_models = [Student]
    serializer_class = StudentAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StudentApplicationViewSet(viewsets.ModelViewSet):
    queryset = StudentApplication.objects.all()
    serializer_class = StudentApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('artist__user__username',)

    def get_queryset(self):
        """
        This view should return a list of all the purchases and create
        an application and Artist when User is not staff
        otherwise Staff get all Users applications
        """
        user = self.request.user
        if not user.is_authenticated():
            return list()
        if user.is_staff:
            # or not user.is_authenticated() WHY ???
            return StudentApplication.objects.all()
        else:
            current_year = datetime.date.today().year
            # is an current inscription
            current_year_application = StudentApplication.objects.filter(
                artist__user=user.id,
                created_on__year=current_year
            )
            if not current_year_application:
                # take the artist
                user_artist = Artist.objects.filter(user=user.id)
                if not user_artist:
                    # if not, ceate it
                    user_artist = Artist(user=user)
                    user_artist.save()
                else:
                    # take the first one
                    user_artist = user_artist[0]
                # create application
                student_application = StudentApplication(artist=user_artist)
                student_application.save()

            return StudentApplication.objects.filter(artist__user=user.id)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        # candidate can't update candidature when she's expired, admin can !
        candidature_expiration_date = datetime.datetime.combine(
            StudentApplicationSetup.objects.filter(is_current_setup=True).first().candidature_date_end,
            datetime.datetime.min.time()
        )
        candidature_hasexpired = candidature_expiration_date < datetime.datetime.now()
        if candidature_hasexpired and not user.is_staff:
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
                request.data.get('physical_content_received'))
        ):
            errors = {'Error': 'Field permission denied'}
            return Response(errors, status=status.HTTP_403_FORBIDDEN)

        # send email when candidature is complete
        if(request.data.get('application_completed')):
            application = self.get_object()
            send_candidature_completed_email_to_user(request, user, application)
            send_candidature_completed_email_to_admin(request, user, application)
        # basic update
        return super(self.__class__, self).update(request, *args, **kwargs)
