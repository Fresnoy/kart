from rest_framework import viewsets

from .models import Gallery, Medium
from .serializers import GallerySerializer, MediumSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

class MediumViewSet(viewsets.ModelViewSet):
    queryset = Medium.objects.all()
    serializer_class = MediumSerializer
