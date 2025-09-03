from tastypie import fields
from tastypie.resources import ModelResource

from .models import Gallery, Medium


class MediumResource(ModelResource):
    class Meta:
        queryset = Medium.objects.all()
        resource_name = 'asset/medium'
    # empty fields when media is private
    def dehydrate(self, bundle):
        if bundle.obj.private and not bundle.request.user.is_authenticated:
            bundle.data['label'] = "Private Media"
            bundle.data['description'] = "Private Media Description"
            bundle.data['picture'] = None
            bundle.data['medium_url'] = None
            bundle.data['file'] = None
        return bundle


class GalleryResource(ModelResource):
    class Meta:
        queryset = Gallery.objects.all()
        resource_name = 'asset/gallery'
    media = fields.ToManyField(MediumResource, 'media', full=True)
