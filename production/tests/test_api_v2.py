import pytest

from django.urls import reverse
from common.tests.conftest import *  # noqa
from diffusion.tests.conftest import *  # noqa
from people.tests.conftest import *  # noqa
from utils.tests.utils import (
    IsArtistOrReadOnlyModelViewSetMixin,
    ReadOnlyModelViewSetMixin,
    HelpTestForModelViewSet,
    parametrize_user_roles,
)


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestArtworkViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/artwork'

    fixtures = ['installation', 'film', 'award']

    expected_list_size = 2
    expected_fields = ['production_date', 'authors', 'title', 'description_fr']

    mutate_fields = ['title']
    put_fields = ['type', 'authors', 'genres', 'production_date', 'title']
    built_fields = {
        'type': lambda x: 'Installation',
        'authors': lambda x: [reverse('artist-detail', kwargs={'pk': x.authors.first().pk})],
        'genres': lambda x: [],
    }

    def target(self):
        return self.installation

    def requestor(self, role):
        return self.installation.authors.first().user


@pytest.mark.django_db
class TestFilmViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/film'

    fixtures = ['film']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'genres', 'aspect_ratio']

    mutate_fields = ['title']
    put_fields = ['authors', 'genres', 'production_date', 'title']
    built_fields = {
        'authors': lambda x: [reverse('artist-detail', kwargs={'pk': x.authors.first().pk})],
        'genres': lambda x: [],
    }

    def target(self):
        return self.film

    def requestor(self, role):
        return self.film.authors.first().user


@pytest.mark.django_db
class TestInstallationViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/installation'

    fixtures = ['installation']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'genres', 'technical_description']

    mutate_fields = ['title']
    put_fields = ['authors', 'genres', 'production_date', 'title']
    built_fields = {
        'authors': lambda x: [reverse('artist-detail', kwargs={'pk': x.authors.first().pk})],
        'genres': lambda x: [],
    }

    def target(self):
        return self.installation

    def requestor(self, role):
        return self.installation.authors.first().user


@pytest.mark.django_db
class TestPerformanceViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/performance'

    fixtures = ['performance']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors']

    mutate_fields = ['title']
    put_fields = ['authors', 'genres', 'production_date', 'title']
    built_fields = {
        'authors': lambda x: [reverse('artist-detail', kwargs={'pk': x.authors.first().pk})],
        'genres': lambda x: [],
    }

    def target(self):
        return self.performance

    def requestor(self, role):
        return self.performance.authors.first().user


@pytest.mark.django_db
class TestEventViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/event'

    fixtures = ['user', 'event']

    expected_list_size = 1
    expected_fields = ['type', 'place', 'installations', 'films', 'performances']

    mutate_fields = ['title']
    put_fields = ['starting_date', 'title', 'type']

    def target(self):
        return self.event


@pytest.mark.django_db
class TestItineraryViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/itinerary'

    fixtures = ['user', 'itinerary']

    expected_list_size = 1
    expected_fields = ['label_fr', 'label_en', 'artworks']

    mutate_fields = ['label_fr']
    put_fields = [
        'description_en',
        'description_fr',
        'event',
        'label_en',
        'label_fr',
    ]
    hyperlinked_fields = {'event': 'event'}

    def target(self):
        return self.itinerary


@pytest.mark.django_db
class TestFilmGenreViewSet(IsArtistOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/film-genre'

    fixtures = ['film_genre', 'artist', 'user']

    expected_list_size = 1
    expected_fields = ['label']

    mutate_fields = ['label']


@pytest.mark.django_db
class TestInstallationGenreViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/installation-genre'

    fixtures = ['installation_genre', 'user']

    expected_list_size = 1
    expected_fields = ['label']

    mutate_fields = ['label']

    def target(self):
        return self.installation_genre


@pytest.mark.django_db
class TestCollaboratorViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/collaborator'

    fixtures = ['production_staff_task']

    expected_list_size = 1
    expected_fields = ['staff', 'task']

    mutate_fields = ['staff']
    put_fields = ['staff', 'task']
    hyperlinked_fields = {'staff': 'staff'}
    built_fields = {
        'task': lambda x: {'label': x.task.label, 'description': x.task.description}
    }

    def target(self):
        return self.production_staff_task

    def requestor(self, role):
        return self.production_staff_task.staff.user


@pytest.mark.django_db
class TestPartnerViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/partner'

    fixtures = ['production_organization_task', 'user']

    expected_list_size = 1
    expected_fields = ['organization', 'task']

    mutate_fields = ['organization']
    put_fields = ['organization', 'task']
    hyperlinked_fields = {'organization': 'organization'}
    built_fields = {
        'task': lambda x: {'label': x.task.label, 'description': x.task.description}
    }

    def target(self):
        return self.production_organization_task


@pytest.mark.django_db
class TestOrganizationTaskViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    # FIXME people?
    viewset_name = 'people/organization-staff'

    fixtures = ['organization_task', 'user']

    expected_list_size = 1
    expected_fields = ['label', 'description']

    mutate_fields = ['label']
    put_fields = ['label', 'description']

    def target(self):
        return self.organization_task


@pytest.mark.django_db
class TestFilmKeywordsViewSet(ReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'production/film-keywords'

    fixtures = ['film_keyword', 'user']

    expected_list_size = 1
    expected_fields = ['name', 'slug']

    mutate_fields = ['name']
    put_fields = ['name', 'slug']

    def target(self):
        return self.film_keyword
