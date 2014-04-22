from tastypie import fields
from tastypie.resources import ModelResource

from .models import Place

class PlaceResource(ModelResource):
    class Meta:
        queryset = Place.objects.all()
        resource_name = 'diffusion/place'

