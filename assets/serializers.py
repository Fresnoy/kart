from rest_framework import serializers

from .models import Gallery, Medium


class MediumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medium
        fields = (
                    'id',
                    'position',
                    'label',
                    'description',
                    'picture',
                    'medium_url',
                    'file',
                    'url',
                    'gallery',
                    'updated_on',
                )


class GallerySerializer(serializers.HyperlinkedModelSerializer):

    media = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='medium-detail'
    )

    class Meta:
        model = Gallery
        fields = ('id', 'url', 'label', 'description', 'media', )
