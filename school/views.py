from datetime import date

from rest_framework import viewsets, permissions
from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet

from people.models import Artist

from .models import Promotion, Student, StudentApplication
from .serializers import (PromotionSerializer, StudentSerializer,
                          StudentAutocompleteSerializer, StudentApplicationSerializer
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

    def get_queryset(self):
        """
        This view should return a list of all the purchases and create
        an application and Artist when User is not staff
        otherwise Staff get all Users applications
        """
        user = self.request.user

        if user.is_staff or not user.is_authenticated():
            return StudentApplication.objects.all()
        else:

            current_year = date.today().year
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
