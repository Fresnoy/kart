from rest_framework import serializers

from .models import BTBeacon, Website


class BTBeaconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BTBeacon


class WebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Website
