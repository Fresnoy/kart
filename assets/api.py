from tastypie import fields
from tastypie.resources import ModelResource

from .models import Gallery, Medium


class MediumResource(ModelResource):
    class Meta:
        queryset = Medium.objects.all()
        resource_name = 'asset/medium'


class GalleryResource(ModelResource):
    class Meta:
        queryset = Gallery.objects.all()
        resource_name = 'asset/gallery'

    media = fields.ToManyField(MediumResource, 'media', full=True)
    



        