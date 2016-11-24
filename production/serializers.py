from rest_framework import serializers

from .models import (
    Film, FilmGenre, Installation,
    Performance, InstallationGenre,
    Event, Itinerary,StaffTask, ProductionStaffTask, ProductionOrganizationTask,
)
from people.models import Staff
from people.serializers import StaffSerializer


class StaffTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTask


class ProductionStaffTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionStaffTask
        fields = ('staff', 'task')

    staff = StaffSerializer()
    task = StaffTaskSerializer(many=True, read_only=True)


class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductionOrganizationTask


class InstallationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Installation
        exclude = ('polymorphic_ctype',)


class FilmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        exclude = ('polymorphic_ctype',)

    collaborators = ProductionStaffTaskSerializer(read_only=True)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        exclude = ('polymorphic_ctype',)


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Performance
        exclude = ('polymorphic_ctype',)


class FilmGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilmGenre


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Itinerary


class InstallationGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstallationGenre
