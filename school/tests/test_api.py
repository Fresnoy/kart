import pytest

from utils.tests.conftest import *  # noqa
from utils.tests.utils import (
    HaystaskSearchModelRessourceMixin,
    HelpTestForReadOnlyModelRessource,
    parametrize_user_roles,
)

from .. import api


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestPromotionRessource(HelpTestForReadOnlyModelRessource):
    model = api.PromotionResource

    fixtures = ['user', 'promotion']

    expected_list_size = 1
    expected_fields = ['starting_year', 'ending_year']

    def target(self):
        return self.promotion

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestStudentRessource(HaystaskSearchModelRessourceMixin, HelpTestForReadOnlyModelRessource):
    model = api.StudentResource

    fixtures = ['student']

    expected_list_size = 1
    expected_fields = ['number', 'promotion', 'artist']

    search_field = 'number'

    def target(self):
        return self.student

    def requestor(self):
        return self.student.user

    def test_user__last_name__istartswith_search(self, client, user_role, request):
        self.setup_fixtures(request)

        data = {'user__last_name__istartswith': self.student.user.last_name[0]}
        kwargs = self.prepare_request(client, user_role, data)
        response = client.get(self.base_url, **kwargs)

        if self.thats_all_folk('list', response):
            return

        answer = response.json()

        assert "meta" in answer
        assert "objects" in answer
        assert len(answer["objects"]) == 1


@pytest.mark.django_db
class TestStudentApplicationRessource(HelpTestForReadOnlyModelRessource):
    model = api.StudentApplicationResource

    fixtures = ['student_application']

    expected_list_size = 0
    expected_fields = []

    methods_behavior = {
        'list': 200,
        'get': 401,
        'patch': 401,
        'put': 401,
        'post': 501,
        'delete': 401,
    }

    def target(self):
        return self.student_application

    def requestor(self):
        return self.student_application.artist.user
