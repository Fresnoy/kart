from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from .models import Place, Award, MetaAward
from production.serializers import StaffTaskSerializer


class PlaceSerializer(CountryFieldMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place


class MetaAwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetaAward

    task = StaffTaskSerializer()


class AwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Award

    artwork = serializers.HyperlinkedRelatedField(read_only=True, view_name='artwork-detail')
