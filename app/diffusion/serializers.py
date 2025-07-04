from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from .models import Place, Award, MetaAward, MetaEvent, Diffusion
from production.models import Artwork


class PlaceSerializer(CountryFieldMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class MetaAwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetaAward
        fields = '__all__'

    # Commented for create metaAward instances by api
    # task = StaffTaskSerializer()


class AwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

    artwork = serializers.HyperlinkedRelatedField(queryset=Artwork.objects.all(), view_name='artwork-detail', many=True)


class MetaEventSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetaEvent
        fields = '__all__'

    keywords = TagListSerializerField()


class DiffusionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diffusion
        fields = '__all__'
