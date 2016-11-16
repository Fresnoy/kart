from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Artist, Staff, Organization, FresnoyProfile


class FresnoyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FresnoyProfile

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        exclude = ('updated_on',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile')

    profile = FresnoyProfileSerializer()


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
