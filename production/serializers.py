from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (
    Film, FilmGenre, Installation,
    Performance, InstallationGenre,
    Event, Itinerary, StaffTask, OrganizationTask,
    ProductionStaffTask, ProductionOrganizationTask,
    Artwork
)
from people.serializers import StaffSerializer


class OrganizationTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganizationTask


class StaffTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StaffTask
        fields = ('label', 'description')


class ProductionStaffTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductionStaffTask
        fields = ('staff', 'task')

    staff = StaffSerializer()
    task = StaffTaskSerializer()


class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductionOrganizationTask
        fields = ('organization', 'task')


class ArtworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artwork

    diffusions = serializers.HyperlinkedRelatedField(source='events',
                                                     read_only=True,
                                                     view_name='event-detail',
                                                     many=True)
    award = serializers.HyperlinkedRelatedField(view_name='award-detail', read_only=True, many=True)


class InstallationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Installation
        exclude = ('polymorphic_ctype',)

    collaborators = ProductionStaffTaskSerializer(source='staff_tasks', many=True)
    partners = PartnerSerializer(source='organization_tasks', many=True)
    diffusions = serializers.HyperlinkedRelatedField(source='events',
                                                     read_only=True,
                                                     view_name='event-detail',
                                                     many=True)
    award = serializers.HyperlinkedRelatedField(view_name='award-detail', read_only=True, many=True)


class FilmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        exclude = ('polymorphic_ctype',)

    collaborators = ProductionStaffTaskSerializer(source='staff_tasks', many=True)
    partners = PartnerSerializer(source='organization_tasks', many=True)
    diffusions = serializers.HyperlinkedRelatedField(source='events',
                                                     read_only=True,
                                                     view_name='event-detail',
                                                     many=True)
    award = serializers.HyperlinkedRelatedField(view_name='award-detail', read_only=True, many=True)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        exclude = ('polymorphic_ctype',)

    partners = PartnerSerializer(source='organization_tasks', many=True)
    parent_event = serializers.HyperlinkedRelatedField(view_name='event-detail', read_only=True, many=True)
    meta_award = serializers.HyperlinkedRelatedField(view_name='award-detail', read_only=True, many=True)


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Performance
        exclude = ('polymorphic_ctype',)

    collaborators = ProductionStaffTaskSerializer(source='staff_tasks', many=True)
    partners = PartnerSerializer(source='organization_tasks', many=True)
    diffusions = serializers.HyperlinkedRelatedField(source='events',
                                                     read_only=True,
                                                     view_name='event-detail',
                                                     many=True)
    award = serializers.HyperlinkedRelatedField(view_name='metaaward-detail', read_only=True, many=True)


class ArtworkPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'type'
    model_serializer_mapping = {
        Artwork: ArtworkSerializer,
        Film: FilmSerializer,
        Installation: InstallationSerializer,
        Performance: PerformanceSerializer
    }


class FilmGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilmGenre


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Itinerary


class InstallationGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstallationGenre
