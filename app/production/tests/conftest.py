import pytest

from people.tests.conftest import *  # noqa
from utils.tests.conftest import *  # noqa

from . import factories


@pytest.fixture
def staff_task(db_ready):
    return factories.StaffTaskFactory()


@pytest.fixture
def production_staff_task(db_ready):
    return factories.ProductionStaffTaskFactory()


@pytest.fixture
def production(db_ready):
    return factories.ProductionFactory()


@pytest.fixture
def organization_task(db_ready):
    return factories.OrganizationTaskFactory()


@pytest.fixture
def production_organization_task(db_ready):
    return factories.ProductionOrganizationTaskFactory()


@pytest.fixture
def anonymous_artwork(db_ready):
    return factories.ArtworkFactory(authors=[])


@pytest.fixture
def artwork(db_ready, artist):
    return factories.ArtworkFactory(authors=[artist])


@pytest.fixture
def film_keyword(db_ready, film):
    tag = factories.TagFactory()
    film.keywords.add(tag)
    return tag


@pytest.fixture
def film_genre(db_ready):
    return factories.FilmGenreFactory()


@pytest.fixture
def film(db_ready, artist):
    return factories.FilmFactory(authors=[artist])


@pytest.fixture
def installation_genre(db_ready):
    return factories.InstallationGenreFactory()


@pytest.fixture
def installation(db_ready, artist):
    return factories.InstallationFactory(authors=[artist])


@pytest.fixture
def performance(db_ready, artist):
    return factories.PerformanceFactory(authors=[artist])


@pytest.fixture
def event(db_ready):
    return factories.EventFactory()


@pytest.fixture
def main_event(db_ready, event):
    return factories.EventFactory(main_event=True, subevents=[event])


@pytest.fixture
def itinerary(db_ready):
    return factories.ItineraryFactory()


@pytest.fixture
def exhibition(db_ready):
    return factories.EventFactory(type='EXHIB')
