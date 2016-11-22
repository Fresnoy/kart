from django.contrib.auth.models import User
from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from .models import Artist, Staff, Organization, FresnoyProfile



class FresnoyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FresnoyProfile
        #exclude = ('user')

    birthplace_country = CountryField()
    homeland_country = CountryField()
    residence_country = CountryField()

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
