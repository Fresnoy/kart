from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from .models import Place, Award, Reward
from production.serializers import StaffTaskSerializer


class PlaceSerializer(CountryFieldMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place


class AwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Award

    task = StaffTaskSerializer()


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reward

    artwork = serializers.HyperlinkedRelatedField(read_only=True, view_name='artwork-detail')
