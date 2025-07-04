import pytest

from people.tests.conftest import *  # noqa
from utils.tests.utils import (
    IsArtistOrReadOnlyModelViewSetMixin,
    HelpTestForModelViewSet,
    parametrize_user_roles,
)


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestMediumViewSet(IsArtistOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'assets/medium'

    fixtures = ['medium', 'artist', 'user']

    expected_list_size = 1
    expected_fields = ['medium_url', 'gallery']

    mutate_fields = ['label']
    put_fields = ['gallery']
    hyperlinked_fields = {'gallery': 'gallery'}


@pytest.mark.django_db
class TestGalleryViewSet(IsArtistOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'assets/gallery'

    fixtures = ['gallery', 'artist', 'user']

    expected_list_size = 1
    expected_fields = ['media', 'url']

    mutate_fields = ['label']
    put_fields = ['label', 'description']
