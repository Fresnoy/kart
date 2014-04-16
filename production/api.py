from tastypie.resources import ModelResource
from .models import Installation, Film, Event

class InstallationResource(ModelResource):
    class Meta:
        queryset = Installation.objects.all()
        resource_name = 'production/installation'

class FilmResource(ModelResource):
    class Meta:
        queryset = Film.objects.all()
        resource_name = 'production/film'

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'production/event'
        