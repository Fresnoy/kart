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

    # empty medium when private
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.private and not self.context['request'].user.is_authenticated:
            representation['label'] = "Private Media"
            representation['description'] = "Private Media Description"
            representation['picture'] = None
            representation['medium_url'] = None
            representation['file'] = None
        return representation


class GallerySerializer(serializers.HyperlinkedModelSerializer):

    media = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='medium-detail'
    )

    class Meta:
        model = Gallery
        fields = ('id', 'url', 'label', 'description', 'media', )
