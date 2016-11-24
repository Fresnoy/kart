from django.contrib.auth.models import User
from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from .models import Artist, Staff, Organization, FresnoyProfile



class FresnoyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FresnoyProfile
        #exclude = ('user',)

    id = serializers.ReadOnlyField()
    birthplace_country = CountryField(default="FR")
    homeland_country = CountryField(default="FR")
    residence_country = CountryField(default="FR")

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        exclude = ('updated_on',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', "profile")

    profile = FresnoyProfileSerializer()

    


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff
        #fields = ('staff',)

    #user = FresnoyProfileSerializer()

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
