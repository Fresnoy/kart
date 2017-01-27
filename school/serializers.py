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
        fields = ('id',
                  'url',
                  'artist',
                  'current_year_application_count',
                  'identity_card',
                  'first_time',
                  'last_application_year',
                  'remote_interview',
                  'remote_interview_type',
                  'remote_interview_info',
                  'master_degree',
                  'cursus_justifications',
                  'considered_project_1',
                  'artistic_referencies_project_1',
                  'considered_project_2',
                  'artistic_referencies_project_2',
                  'presentation_video',
                  'physical_content',
                  'physical_content_description',
                  'physical_content_received',
                  'remark',
                  'application_completed',
                  'application_complete',
                  'selected_for_interview',
                  'selected',
                  'wait_listed',
                  'created_on',
                  'updated_on',)
