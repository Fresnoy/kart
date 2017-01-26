from django.contrib.auth.models import User
from rest_framework import serializers

from django_countries.serializer_fields import CountryField

from .models import Artist, Staff, Organization, FresnoyProfile


class PrivateStringField(serializers.Field):

    def to_representation(self, obj):
        return obj

    def get_attribute(self, instance):
        if self.context['request'].user.is_authenticated():
            return super(PrivateStringField, self).get_attribute(instance)
        return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        if self.context['request'].user.is_authenticated():
            return data
        return ""


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
            "homeland_phone",
            "residence_phone",
            "residence_country",
            "residence_address",
            "social_insurance_number",
            "family_status",
        )

    id = serializers.ReadOnlyField()
    birthplace_country = CountryField(default="")
    homeland_phone = PrivateStringField()
    homeland_country = CountryField(default="")
    social_insurance_number = PrivateStringField()
    residence_phone = PrivateStringField()
    residence_country = CountryField(default="")


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, min_length=4, required=True)
    first_name = serializers.CharField(max_length=30, min_length=2, required=True)
    last_name = serializers.CharField(max_length=30, min_length=2, required=True)
    email = serializers.EmailField(max_length=30, min_length=2, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email', 'profile')

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


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        exclude = ('updated_on',)


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff
        # fields = ('staff',)

    # user = FresnoyProfileSerializer()


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
