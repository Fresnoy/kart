from rest_framework import viewsets, permissions

from .models import BTBeacon, Website
from .serializers import BTBeaconSerializer, WebsiteSerializer


class BTBeaconViewSet(viewsets.ModelViewSet):
    queryset = BTBeacon.objects.all()
    serializer_class = BTBeaconSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
