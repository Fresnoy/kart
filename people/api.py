from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from common.api import WebsiteResource

from .models import Artist, Staff, Organization

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.exclude(pk=-1) # Exclude anonymous user
        detail_uri_name = 'username'
        resource_name = 'people/user'
        fields = ['username', 'first_name', 'last_name']

        filtering = {
            'first_name': ALL,
            'last_name': ALL
        }

    def dehydrate(self, bundle):
        bundle.data['photo'] = bundle.obj.profile.photo
        bundle.data['birthdate'] = bundle.obj.profile.birthdate
        bundle.data['birthplace'] = bundle.obj.profile.birthplace
        bundle.data['cursus'] = bundle.obj.profile.cursus
        #bundle.data['first_name'] = bundle.obj.user.first_name
        #bundle.data['last_name'] = bundle.obj.user.last_name
        return bundle


class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.all()
        resource_name = 'people/artist'
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'resource_uri': ALL
        }

        fields = ['id', 'nickname', 'bio_short_fr', 'bio_short_en', 'bio_fr', 'bio_en', 'twitter_account', 'facebook_profile']

    websites = fields.ToManyField(WebsiteResource, 'websites', full=True)
    user = fields.ForeignKey(UserResource, 'user', full=True)
    artworks = fields.ToManyField('production.api.ArtworkResource', 'artworks', full=False, null=True, use_in=['detail'])

class StaffResource(ModelResource):
    class Meta:
        queryset = Staff.objects.all()
        resource_name = 'people/staff'

class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'people/organization'
