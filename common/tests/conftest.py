import pytest

from . import factories


@pytest.fixture
def website(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.WebsiteFactory()


@pytest.fixture
def btbeacon(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.BTBeaconFactory()
