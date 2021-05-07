import pytest

from people.tests.conftest import *  # noqa

from . import factories


@pytest.fixture
def staff_task(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.StaffTaskFactory()


@pytest.fixture
def production_staff_task(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.ProductionStaffTaskFactory()


@pytest.fixture
def production(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.ProductionFactory()


@pytest.fixture
def anonymous_artwork(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.ArtworkFactory(authors=[])


@pytest.fixture
def artwork(django_db_setup, django_db_blocker, artist):
    with django_db_blocker.unblock():
        return factories.ArtworkFactory(authors=[artist])


@pytest.fixture
def film_genre(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.FilmGenreFactory()


@pytest.fixture
def installation_genre(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.InstallationGenreFactory()


@pytest.fixture
def event(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.EventFactory()


@pytest.fixture
def main_event(django_db_setup, django_db_blocker, event):
    with django_db_blocker.unblock():
        return factories.EventFactory(main_event=True, subevents=[event])


@pytest.fixture
def itinerary(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.ItineraryFactory()
