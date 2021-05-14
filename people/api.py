# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from common.api import WebsiteResource
from .models import Artist, Staff, Organization


# django-guardian anonymous user
try:
    ANONYMOUS_USER_NAME = settings.ANONYMOUS_USER_NAME
except AttributeError:
    ANONYMOUS_USER_NAME = "AnonymousUser"


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.exclude(username=ANONYMOUS_USER_NAME)  # Exclude anonymous user
        detail_uri_name = 'username'
        resource_name = 'people/user'
        fields = ['username', 'first_name', 'last_name', 'id', ]
        filtering = {
            'first_name': ALL,
            'last_name': ALL
        }

    def dehydrate(self, bundle):
        if hasattr(bundle.obj, 'profile'):
            bundle.data['photo'] = bundle.obj.profile.photo
            bundle.data['birthdate'] = bundle.obj.profile.birthdate
            bundle.data['birthplace'] = bundle.obj.profile.birthplace
            bundle.data['cursus'] = bundle.obj.profile.cursus
            bundle.data['gender'] = bundle.obj.profile.gender
            # Nationality : country code separated by commas
            bundle.data['nationality'] = bundle.obj.profile.nationality
            bundle.data['homeland_country'] = bundle.obj.profile.homeland_country
            bundle.data['birthplace_country'] = bundle.obj.profile.birthplace_country

        return bundle


class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.all()
        resource_name = 'people/artist'
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'resource_uri': ALL
        }

        fields = ['id', 'nickname', 'bio_short_fr', 'bio_short_en',
                  'bio_fr', 'bio_en', 'twitter_account', 'facebook_profile']

    websites = fields.ToManyField(WebsiteResource, 'websites', full=True)
    user = fields.ForeignKey(UserResource, 'user', full=True)
    artworks = fields.ToManyField('production.api.ArtworkResource', 'artworks',
                                  full=False, null=True, use_in=['detail'])


class StaffResource(ModelResource):
    class Meta:
        queryset = Staff.objects.all()
        resource_name = 'people/staff'
        fields = ('user',)

    user = fields.ForeignKey(UserResource, 'user', full=True)


class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'people/organization'
