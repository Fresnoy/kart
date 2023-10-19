from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializerMixin
from dj_rest_auth.serializers import PasswordResetSerializer

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from people.serializers import PublicUserSerializer

from .models import (Promotion, Student, PhdStudent, ScienceStudent, TeachingArtist,
                     VisitingStudent, StudentApplication, StudentApplicationSetup, AdminStudentApplication)
from .search_indexes import StudentIndex
from .utils import candidature_close


class PhdStudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhdStudent
        fields = '__all__'


class ScienceStudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScienceStudent
        fields = '__all__'


class VisitingStudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VisitingStudent
        fields = '__all__'


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        # depth = 1
    user_infos = PublicUserSerializer(source='user', read_only=True)
    phd_student = PhdStudentSerializer(required=False,)
    science_student = ScienceStudentSerializer(required=False,)

    user = serializers.HyperlinkedRelatedField(view_name="user-detail",
                                               queryset=User.objects.all(), write_only=True)


class TeachingArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeachingArtist
        fields = '__all__'


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class StudentAutocompleteSerializer(HaystackSerializerMixin, StudentSerializer):
    class Meta(StudentSerializer.Meta):
        index_classes = [StudentIndex]
        search_fields = ("content_auto", )
        fields = ["url", "number", "graduate", "promotion", "artist", "user", ]
        field_aliases = {
            "q": "content_auto"
        }
        depth = 1

    user = PublicUserSerializer()


class StudentApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentApplication
        fields = ('id',
                  'url',
                  'campaign',
                  'artist',
                  'current_year_application_count',
                  'identity_card',
                  'INE',
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
                  'created_on',
                  'updated_on',)


class AdminStudentApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdminStudentApplication
        fields = ('id',
                  'application',
                  'application_complete',
                  'wait_listed_for_interview',
                  'position_in_interview_waitlist',
                  'selected_for_interview',
                  'interview_date',
                  'selected',
                  'unselected',
                  'wait_listed',
                  'position_in_waitlist',
                  'observation',)


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


class StudentPasswordResetSerializer(PasswordResetSerializer):

    @property
    def password_reset_form_class(self):
        return PasswordResetForm

    def get_email_options(self):
        return {
            'subject_template_name': 'emails/account/password_reset_subject.txt',
            'email_template_name': 'emails/account/password_reset_email.txt',
            'html_email_template_name': 'emails/account/password_reset_email.html',
        }
