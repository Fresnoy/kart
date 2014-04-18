from tastypie import fields
from tastypie.resources import ModelResource

from assets.api import GalleryResource
from people.api import ArtistResource

from .models import Installation, Film, Performance

class ArtworkResource(ModelResource):
    process_galleries = fields.ToManyField(GalleryResource, 'process_galleries', full=True)
    mediation_galleries = fields.ToManyField(GalleryResource, 'mediation_galleries', full=True)
    in_situ_galleries = fields.ToManyField(GalleryResource, 'in_situ_galleries', full=True)
    
    authors = fields.ToManyField(ArtistResource, 'authors')

class InstallationResource(ArtworkResource):
    class Meta:
        queryset = Installation.objects.all()
        resource_name = 'production/installation'

class FilmResource(ArtworkResource):
    class Meta:
        queryset = Film.objects.all()
        resource_name = 'production/film'

class PerformanceResource(ArtworkResource):
    class Meta:
        queryset = Performance.objects.all()
        resource_name = 'production/performance'

