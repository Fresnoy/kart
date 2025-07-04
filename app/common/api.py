from tastypie.resources import ModelResource

from .models import Website, BTBeacon


class BTBeaconResource(ModelResource):
    class Meta:
        queryset = BTBeacon.objects.all()


class WebsiteResource(ModelResource):
    class Meta:
        queryset = Website.objects.all()
