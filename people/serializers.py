from django.contrib.auth.models import User
from rest_framework import serializers

from django_countries.serializer_fields import CountryField

from .models import Artist, Staff, Organization, FresnoyProfile


class FresnoyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FresnoyProfile
        # exclude = ('user',)
        fields = (
            "id",
            "photo",
            "gender",
            "cursus",
            "nationality",
            "birthdate",
            "birthplace",
            "birthplace_country",
            "mother_tongue",
            "other_language",
            "homeland_country",
            "homeland_address",
            "homeland_zipcode",
            "homeland_town",
            "homeland_phone",
            "residence_phone",
            "residence_country",
            "residence_zipcode",
            "residence_address",
            "residence_town",
            "social_insurance_number",
            "family_status",
            "is_artist",
            "is_staff",
            "is_student",
        )

    id = serializers.ReadOnlyField()
    birthplace_country = CountryField(default="", allow_blank=True)
    homeland_country = CountryField(default="", allow_blank=True)
    residence_country = CountryField(default="", allow_blank=True)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=4, required=True)
    first_name = serializers.CharField(max_length=150, min_length=2, required=True)
    last_name = serializers.CharField(max_length=150, min_length=2, required=True)
    email = serializers.EmailField(max_length=254, min_length=2, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_superuser', 'url', 'username', 'first_name', 'last_name', 'email', 'profile')

    profile = FresnoyProfileSerializer(required=False)

    def create(self, validated_data):
        return validated_data

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

        # set Values for UserProfile
        for item in profile_data:
            value = profile_data.get(item)
            setattr(instance.profile, item, value)

        instance.profile.save()
        instance.save()

        return instance


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name')


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'url',
            'nickname',
            'bio_short_fr',
            'bio_short_en',
            'bio_fr',
            'bio_en',
            'twitter_account',
            'facebook_profile',
            'user',
            'websites',
        )


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff
        fields = ('user',)

    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
