from rest_framework import serializers

from .models import Place


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
