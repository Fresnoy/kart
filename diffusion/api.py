from tastypie import fields
from tastypie.resources import ModelResource

from .models import Event, Place

class PlaceResource(ModelResource):
    class Meta:
        queryset = Place.objects.all()
        resource_name = 'diffusion/place'

class EventResource(ModelResource):
    place = fields.ForeignKey(PlaceResource, 'place')

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'diffusion/event'