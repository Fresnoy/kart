from tastypie.resources import ModelResource

from .models import Artist, Staff, Organization

class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.all()
        resource_name = 'people/artist'

class StaffResource(ModelResource):
    class Meta:
        queryset = Staff.objects.all()
        resource_name = 'people/staff'

class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'people/organization'