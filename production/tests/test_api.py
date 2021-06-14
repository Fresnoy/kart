import pytest

from diffusion.tests.conftest import *  # noqa
from utils.tests.conftest import *  # noqa
from utils.tests.utils import (
    FilterModelRessourceMixin,
    HaystackSearchModelRessourceMixin,
    HelpTestForReadOnlyModelRessource,
    parametrize_user_roles,
)

from .. import api


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestStaffTaskRessource(HelpTestForReadOnlyModelRessource):
    resource = api.StaffTaskResource

    fixtures = ['staff_task', 'user']

    expected_list_size = 1
    expected_fields = ['label']


@pytest.mark.django_db
class TestArtworkRessource(
    HaystackSearchModelRessourceMixin,
    FilterModelRessourceMixin,
    HelpTestForReadOnlyModelRessource,
):
    resource = api.ArtworkResource

    fixtures = ['installation', 'film', 'award', 'user']

    expected_list_size = 2
    expected_fields = ['production_date', 'authors', 'events']

    search_field = 'title'


@pytest.mark.django_db
class TestInstallationResource(HelpTestForReadOnlyModelRessource):
    resource = api.InstallationResource

    fixtures = ['installation', 'user']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'events', 'genres', 'technical_description']


@pytest.mark.django_db
class TestFilmResource(HelpTestForReadOnlyModelRessource):
    resource = api.FilmResource

    fixtures = ['film', 'user']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'events', 'genres', 'aspect_ratio']


@pytest.mark.django_db
class TestPerformanceResource(HelpTestForReadOnlyModelRessource):
    resource = api.PerformanceResource

    fixtures = ['performance', 'user']

    expected_list_size = 1
    expected_fields = ['production_date', 'authors', 'events']


@pytest.mark.django_db
class TestEventResource(HelpTestForReadOnlyModelRessource):
    resource = api.EventResource

    fixtures = ['event', 'user']

    expected_list_size = 1
    expected_fields = ['type', 'place', 'installations', 'films', 'performances']


@pytest.mark.django_db
class TestItineraryResource(HelpTestForReadOnlyModelRessource):
    resource = api.ItineraryResource

    fixtures = ['itinerary', 'user']

    expected_list_size = 1
    expected_fields = ['label_fr', 'label_en', 'artworks']


@pytest.mark.django_db
class TestExhibitionResource(TestEventResource):
    resource = api.ExhibitionResource

    fixtures = ['exhibition', 'user']

    expected_list_size = 1
    expected_fields = ['type', 'place', 'installations', 'films', 'performances', 'itineraries']
