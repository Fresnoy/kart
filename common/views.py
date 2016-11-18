# Create your views here.
from rest_framework import viewsets

from .models import BTBeacon, Website
from .serializers import BTBeaconSerializer, WebsiteSerializer


class BTBeaconViewSet(viewsets.ModelViewSet):
    queryset = BTBeacon.objects.all()
    serializer_class = BTBeaconSerializer

class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
