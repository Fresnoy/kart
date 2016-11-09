from rest_framework import serializers

from .models import Gallery, Medium


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gallery


class MediumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medium
