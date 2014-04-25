from tastypie import fields
from tastypie.resources import ModelResource

from common.api import WebsiteResource

from .models import Artist, Staff, Organization

class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.all()
        resource_name = 'people/artist'

    websites = fields.ToManyField(WebsiteResource, 'websites', full=True)

class StaffResource(ModelResource):
    class Meta:
        queryset = Staff.objects.all()
        resource_name = 'people/staff'

class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'people/organization'