from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django_countries.serializers import CountryFieldMixin
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from .models import Place, Award, MetaAward, MetaEvent, Diffusion
from production.serializers import StaffTaskSerializer


class PlaceSerializer(CountryFieldMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class MetaAwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetaAward
        fields = '__all__'

    task = StaffTaskSerializer()


class AwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

    artwork = serializers.HyperlinkedRelatedField(read_only=True, view_name='artwork-detail', many=True)


class MetaEventSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetaEvent
        fields = '__all__'

    keywords = TagListSerializerField()


class DiffusionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diffusion
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Diffusion.objects.all(),
                fields=['artwork', 'event']
            )
        ]
