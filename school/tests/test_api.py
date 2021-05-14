import pytest

from utils.tests.conftest import *  # noqa
from utils.tests.utils import HaystaskSearchModelRessourceMixin, HelpTestForReadOnlyModelRessource

from .. import api


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
