from django.contrib.auth.models import User
from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from .models import Artist, Staff, Organization, FresnoyProfile


class FresnoyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FresnoyProfile
        exclude = ('user',)

    #id = serializers.ReadOnlyField()
    birthplace_country = CountryField(default="FR")
    homeland_country = CountryField(default="FR")
    residence_country = CountryField(default="FR")
    #user = serializers(source="user")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email', 'profile')

    profile = FresnoyProfileSerializer(required=False)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)

        # set user in profile
        profile_data["user"] = user

        # save profile
        FresnoyProfile.objects.create(**profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        # Update User data
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        # Update UserProfile data
        if not instance.profile:
            FresnoyProfile.objects.create(user=instance, **profile_data)

        #set Values for UserProfile
        for item in profile_data:
            value = profile_data.get(item)
            setattr(instance.profile, item, value)

        instance.save()
        return instance


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        exclude = ('updated_on',)




class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff
#        fields = ('staff',)
#    user = FresnoyProfileSerializer()


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
