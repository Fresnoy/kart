import pytest

from diffusion.tests.conftest import *  # noqa
from utils.tests.conftest import *  # noqa
from utils.tests.utils import (
    FilterModelRessourceMixin,
    HaystaskSearchModelRessourceMixin,
    HelpTestForReadOnlyModelRessource,
    parametrize_user_roles,
)

from .. import api


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestStaffTaskRessource(HelpTestForReadOnlyModelRessource):
    model = api.StaffTaskResource

    fixtures = ['user', 'staff_task']

    expected_list_size = 1
    expected_fields = ['label']

    def target(self):
        return self.staff_task

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestArtworkRessource(
    HaystaskSearchModelRessourceMixin,
    FilterModelRessourceMixin,
    HelpTestForReadOnlyModelRessource,
):
    model = api.ArtworkResource

    fixtures = ['user', 'installation', 'film', 'award']

    expected_list_size = 2
    expected_fields = ['production_date', 'authors', 'events']

    search_field = 'title'

    def target(self):
        return self.installation

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestInstallationResource(HelpTestForReadOnlyModelRessource):
    model = api.InstallationResource

    fixtures = ['user', 'installation']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'events', 'genres', 'technical_description']

    def target(self):
        return self.installation

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestFilmResource(HelpTestForReadOnlyModelRessource):
    model = api.FilmResource

    fixtures = ['user', 'film']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'events', 'genres', 'aspect_ratio']

    def target(self):
        return self.film

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestPerformanceResource(HelpTestForReadOnlyModelRessource):
    model = api.PerformanceResource

    fixtures = ['user', 'performance']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'events']

    def target(self):
        return self.performance

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestEventResource(HelpTestForReadOnlyModelRessource):
    model = api.EventResource

    fixtures = ['user', 'event']

    expected_list_size = 1
    expected_fields = ['type', 'place', 'installations', 'films', 'performances']

    def target(self):
        return self.event

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestItineraryResource(HelpTestForReadOnlyModelRessource):
    model = api.ItineraryResource

    fixtures = ['user', 'itinerary']

    expected_list_size = 1
    expected_fields = ['label_fr', 'label_en', 'artworks']

    def target(self):
        return self.itinerary

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestExhibitionResource(TestEventResource):
    model = api.ExhibitionResource

    fixtures = ['user', 'exhibition']

    expected_list_size = 1
    expected_fields = ['type', 'place', 'installations', 'films', 'performances', 'itineraries']

    def target(self):
        return self.exhibition

    def requestor(self):
        return self.user
