import pytest

from common.tests.conftest import *  # noqa
from production.tests.conftest import *  # noqa
from utils.tests.utils import HelpTestForReadOnlyModelRessource, parametrize_user_roles

from .. import api


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestPlaceRessource(HelpTestForReadOnlyModelRessource):
    resource = api.PlaceResource

    fixtures = ['place', 'user']

    expected_list_size = 1
    expected_fields = ['name', 'latitude', 'longitude']


@pytest.mark.django_db
class TestAwardRessource(HelpTestForReadOnlyModelRessource):
    resource = api.AwardResource

    fixtures = ['award', 'artist', 'artwork']

    expected_list_size = 1
    expected_fields = ['date', 'meta_award', 'artwork', 'artist']

    def requestor(self, role):
        return self.artist.user


@pytest.mark.django_db
class TestMetaAwardRessource(HelpTestForReadOnlyModelRessource):
    resource = api.MetaAwardResource

    fixtures = ['meta_award', 'user']

    expected_list_size = 1
    expected_fields = ['label', 'event', 'task']
