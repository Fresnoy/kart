import pytest

from uuid import uuid4

from common.tests.conftest import *  # noqa
from diffusion.tests.conftest import *  # noqa
from production.tests.conftest import *  # noqa
from people.tests.conftest import *  # noqa
from school.tests.conftest import *  # noqa
from utils.tests.utils import (
    IsAuthenticatedOrReadOnlyModelViewSetMixin,
    IsArtistOrReadOnlyModelViewSetMixin,
    HelpTestForModelViewSet,
    parametrize_user_roles,
)


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestBTBeaconViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'common/beacon'

    fixtures = ['btbeacon', 'user']

    expected_list_size = 1
    expected_fields = ['rssi_in', 'rssi_out']

    mutate_fields = ['rssi_in']
    put_fields = ['rssi_in', 'rssi_out', 'uuid', 'x', 'y', 'label']
    built_fields = {'uuid': lambda x: str(uuid4())}


@pytest.mark.django_db
class TestWebsiteViewSet(IsArtistOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'common/website'

    fixtures = ['website', 'artist', 'user']

    expected_list_size = 1
    expected_fields = ['url', 'link', 'language', 'title_fr', 'title_en']

    mutate_fields = ['title_fr']
    put_fields = ['link', 'language', 'title_fr', 'title_en']
    hyperlinked_fields = {'url': 'website'}
    renamed_fields = {'link': 'url'}
