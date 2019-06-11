from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer

from .models import Promotion, Student, StudentApplication, StudentApplicationSetup
from .search_indexes import StudentIndex
from .utils import candidature_close


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class StudentAutocompleteSerializer(HaystackSerializer):
    class Meta:
        index_classes = [StudentIndex]
        # fields = ["firstname", "lastname"]
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
                  'campaign',
                  'artist',
                  'current_year_application_count',
                  'identity_card',
                  'first_time',
                  'last_applications_years',
                  'remote_interview',
                  'remote_interview_type',
                  'remote_interview_info',
                  'master_degree',
                  'experience_justification',
                  'cursus_justifications',
                  'curriculum_vitae',
                  'justification_letter',
                  'binomial_application',
                  'binomial_application_with',
                  'considered_project_1',
                  'artistic_referencies_project_1',
                  'considered_project_2',
                  'artistic_referencies_project_2',
                  'doctorate_interest',
                  'presentation_video',
                  'presentation_video_details',
                  'presentation_video_password',
                  'free_document',
                  'remark',
                  'application_completed',
                  'application_complete',
                  'wait_listed_for_interview',
                  'selected_for_interview',
                  'interview_date',
                  'selected',
                  'unselected',
                  'wait_listed',
                  'observation',
                  'created_on',
                  'updated_on',)


class PublicStudentApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentApplication
        fields = ('id',
                  'url',)


class StudentApplicationSetupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentApplicationSetup
        fields = ('id',
                  'url',
                  'promotion',
                  'date_of_birth_max',
                  'candidature_date_start',
                  'candidature_date_end',
                  'candidature_open',
                  'interviews_publish_date',
                  'selected_publish_date',
                  'interviews_start_date',
                  'interviews_end_date',
                  'is_current_setup',
                  'applications',)

    # applications = StudentApplicationSerializer(source='student_application', many=True)
    applications = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='studentapplication-detail'
    )
    candidature_open = serializers.SerializerMethodField()

    def get_candidature_open(self, obj):
        return not candidature_close(obj)
