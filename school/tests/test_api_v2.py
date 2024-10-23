import pytest

from django.urls import reverse
from django.utils import timezone

from people.tests.conftest import *  # noqa
from utils.tests.utils import (
    IgnoreModelViewSetMixin,
    IsArtistOrReadOnlyModelViewSetMixin,
    IsAuthenticatedOrReadOnlyModelViewSetMixin,
    ReadOnlyModelViewSetMixin,
    HelpTestForModelViewSet,
    parametrize_user_roles,
)


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestPromotionViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = "school/promotion"

    fixtures = ["promotion", "user"]

    expected_list_size = 1
    expected_fields = ["starting_year", "ending_year"]

    mutate_fields = ["name"]
    put_fields = ["name", "starting_year", "ending_year"]


@pytest.mark.django_db
class TestStudentViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = "school/student"

    fixtures = ["student", "user", "artist"]

    expected_list_size = 1
    expected_fields = ["number", "promotion"]

    mutate_fields = ["number"]
    put_fields = ["artist", "user"]
    built_fields = {
        "artist": lambda x: reverse("artist-detail", kwargs={"pk": x.artist.pk}),
        "user": lambda x: reverse("user-detail", kwargs={"pk": x.user.pk}),
    }

    def get_data(self, field):
        if field in self.built_fields:
            return self.built_fields[field](self)
        else:
            return super().get_data(field)


@pytest.mark.django_db
class TestStudentApplicationSetupViewSet(IsArtistOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = "school/student-application-setup"

    fixtures = ["student_application_setup", "user", "artist"]

    expected_list_size = 1
    expected_fields = ["candidature_date_start", "candidature_date_end"]

    mutate_fields = ["date_of_birth_max"]
    put_fields = ["candidature_date_start", "candidature_date_end"]


@pytest.mark.django_db
class TestArtistStudentApplicationViewSet(HelpTestForModelViewSet):
    viewset_name = "school/student-application"

    fixtures = ["student_application"]

    expected_list_size = 1
    expected_fields = ["curriculum_vitae"]

    mutate_fields = ["remark"]
    put_fields = []

    _user_roles = ["user"]

    def requestor(self, role):
        return self.student_application.artist.user

    methods_behavior = {
        "list": 200,
        "get": 200,
        "patch": 200,
        "put": 200,
        "post": 409,
        "delete": 204,
    }


@pytest.mark.django_db
class TestUserStudentApplicationViewSet(TestArtistStudentApplicationViewSet):
    fixtures = ["student_application", "user"]

    def requestor(self, role):
        return self.user

    expected_list_size = 0

    methods_behavior = {
        "list": 200,
        "get": 404,
        "patch": 404,
        "put": 404,
        "post": 201,
        "delete": 404,
    }


@pytest.mark.django_db
class TestUserStudentApplicationClosedCampaign(IgnoreModelViewSetMixin, TestUserStudentApplicationViewSet):

    methods_behavior = {
        "post": 403,
        "put": 404,
        "patch": 404,
    }

    def munge_fixtures(self, request):
        self.setup_fixtures(request)

        campaign = self.student_application.campaign
        campaign.is_current_setup = True
        campaign.candidature_date_end = campaign.candidature_date_start
        campaign.save()

        # avoid fixture reinstallation
        self.setup_fixtures = lambda request: None

    def test_patch_on_closed_campaign(self, client, user_role, auth_method, request):
        self.munge_fixtures(request)
        super(TestUserStudentApplicationViewSet, self).test_patch(client, user_role, auth_method, request)

    def test_put_on_closed_campaign(self, client, user_role, auth_method, request):
        self.munge_fixtures(request)
        super(TestUserStudentApplicationViewSet, self).test_put(client, user_role, auth_method, request)

    def test_post_on_closed_campaign(self, client, user_role, auth_method, request):
        self.munge_fixtures(request)
        super(TestUserStudentApplicationViewSet, self).test_post(client, user_role, auth_method, request)

    @pytest.mark.parametrize(
        "action, mailsent",
        [
            ["application_completed", 2],
            # ['application_complete', 1],
            # ['wait_listed_for_interview', 1],
            # ['selected_for_interview', 1],
            # ['unselected', 1],
        ],
    )
    def test_patch_with_mail_action(self, client, admin, student_application, action, mailsent, mailoutbox):
        self.student_application = student_application
        self.student_application.interview_date = timezone.now()
        self.student_application.save()

        client.force_login(admin)

        kwargs = {
            "data": {action: 1},
            "content_type": "application/json",
        }
        response = client.patch("{}/{}".format(self.base_url, self.target_uri_suffix()), **kwargs)
        assert response.status_code == 200
        assert len(mailoutbox) == mailsent

    # def test_abusive_patch_with_mail_action(self, client, artist, student_application):
    #     self.student_application = student_application

    #     client.force_login(artist.user)

    #     kwargs = {
    #         'data': {'selected_for_interview': 1},
    #         'content_type': 'application/json',
    #     }
    #     response = client.patch('{}/{}'.format(self.base_url, self.target_uri_suffix()), **kwargs)
    #     assert response.status_code == 403


@pytest.mark.django_db
class TestAnonymousStudentApplicationViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = "school/student-application"

    fixtures = ["student_application"]

    expected_list_size = 1
    expected_fields = ["id", "url"]

    mutate_fields = ["id"]
    put_fields = []

    _user_roles = [None]
