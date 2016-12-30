from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer

from .models import Promotion, Student, StudentApplication
from .search_indexes import StudentIndex


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion


class StudentAutocompleteSerializer(HaystackSerializer):
    class Meta:
        index_classes = [StudentIndex]
        fields = ["firstname", "lastname"]
        ignore_fields = ["autocomplete"]

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            "q": "autocomplete"
        }


class StudentApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentApplication
        fields = ('id', 'url', 'current_year_application_count', 'first_time', 'last_application_year',
                  'created_on', 'updated_on', 'remote_interview', 'remote_interview_type',
                  'remote_interview_info', 'asynchronous_element', 'asynchronous_element_description',
                  'asynchronous_element_received', 'remark', 'application_completed', 'selected_for_interview',
                  'selected_for_petit_jury', 'selected_for_grand_jury', 'application_complete', 'artist',
                  'administrative_galleries', 'artwork_galleries')

    def update(self, instance, validated_data):

        for item in validated_data:
            if item is "administrative_galleries":
                for gallery in item:
                    instance.administrative_galleries.add(gallery)

            value = validated_data.get(item)
            setattr(instance, item, value)
        instance.save()
        return instance
