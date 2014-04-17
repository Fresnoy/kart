from tastypie import fields
from tastypie.resources import ModelResource

from assets.api import GalleryResource
from people.api import ArtistResource

from .models import Installation, Film, Event

class ProductionResource(ModelResource):
    galleries = fields.ToManyField(GalleryResource, 'galleries', full=True)
    authors = fields.ToManyField(ArtistResource, 'authors')

class InstallationResource(ProductionResource):
    class Meta:
        queryset = Installation.objects.all()
        resource_name = 'production/installation'

class FilmResource(ProductionResource):
    class Meta:
        queryset = Film.objects.all()
        resource_name = 'production/film'

class EventResource(ProductionResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'production/event'
        