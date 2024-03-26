import pytest
from django.urls import reverse

from utils.tests.utils import (
    IsAuthenticatedOrReadOnlyModelViewSetMixin,
    HelpTestForModelViewSet,
    parametrize_user_roles,
)


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestPlaceViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'diffusion/place'

    fixtures = ['place', 'user']

    expected_list_size = 1
    expected_fields = ['latitude', 'longitude']

    mutate_fields = ['name']


@pytest.mark.django_db
class TestAwardViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'diffusion/award'

    fixtures = ['award', 'user', 'artwork']

    put_fields = ['artwork', ]
    built_fields = {
        'artwork': lambda x: [reverse('artwork-detail', kwargs={'pk': x.artwork.first().pk})],
    }

    expected_list_size = 1
    expected_fields = ['artwork', 'meta_award', 'event']

    mutate_fields = ['note']


@pytest.mark.django_db
class TestMetaAwardViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'diffusion/meta-award'

    fixtures = ['meta_award', 'user']

    expected_list_size = 1
    expected_fields = ['event', 'type', 'task']

    mutate_fields = ['label']
    built_fields = {
        'task': lambda x: {'label': x.task.label, 'description': x.task.description}
    }

    @pytest.mark.skip(reason="Putting and posting are impossible")
    def test_put(self):
        return

    @pytest.mark.skip(reason="Putting and posting are impossible")
    def test_post(self):
        return


@pytest.mark.django_db
class TestMetaEventViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'diffusion/meta-event'

    fixtures = ['meta_event', 'user']

    expected_list_size = 1
    expected_fields = ['keywords', 'genres']

    mutate_fields = ['genres']
    put_fields = ['genres', 'keywords']
    built_fields = {
        'keywords': lambda x: [x.keywords.name]
    }

    @pytest.mark.skip(reason="Posting seems impossible")
    def test_post(self):
        return


@pytest.mark.django_db
class TestDiffusionViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'diffusion/diffusion'

    fixtures = ['diffusion', 'user']

    expected_list_size = 1
    expected_fields = ['on_competition', 'event', 'artwork']

    mutate_fields = ['on_competition']
    put_fields = []

    @pytest.mark.skip(reason="Posting seems impossible")
    def test_post(self):
        return
