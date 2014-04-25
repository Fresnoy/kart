from tastypie import fields
from tastypie.resources import ModelResource

from .models import Website

class WebsiteResource(ModelResource):
    class Meta:
        queryset = Website.objects.all()

