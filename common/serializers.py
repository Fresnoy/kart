from rest_framework import serializers

from .models import BTBeacon, Website


class BTBeaconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BTBeacon
        fields = '__all__'


class WebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Website
        fields = (
            "id",
            "url",
            "link",
            "title_fr",
            "title_en",
            "language",
        )
    url = serializers.HyperlinkedIdentityField(view_name="website-detail")
    link = serializers.URLField(source='url')
