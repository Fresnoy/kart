from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Artist, Staff, Organization, FresnoyProfile


class FresnoyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FresnoyProfile
        #exclude = ('user')


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        exclude = ('updated_on',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'profile')
        #fields = ('id','first_name', 'last_name', 'email')

    profile = FresnoyProfileSerializer()


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff
        #fields = ('staff',)

    #user = FresnoyProfileSerializer()

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
