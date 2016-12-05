from rest_framework import viewsets, permissions

from .models import Gallery, Medium
from .serializers import GallerySerializer, MediumSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MediumViewSet(viewsets.ModelViewSet):
    queryset = Medium.objects.all()
    serializer_class = MediumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
