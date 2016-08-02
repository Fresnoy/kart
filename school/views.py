from rest_framework import viewsets
from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet

from .models import Promotion, Student
from .serializers import (PromotionSerializer, StudentSerializer,
                          StudentAutocompleteSerializer)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentAutocompleteSearchViewSet(HaystackViewSet):
    index_models = [Student]
    serializer_class = StudentAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
