from tastypie.resources import ModelResource
from .models import Installation

class InstallationResource(ModelResource):
    class Meta:
        queryset = Installation.objects.all()
        resource_name = 'installation'
