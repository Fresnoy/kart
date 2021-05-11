import pytest

from utils.tests.conftest import *  # noqa

from . import factories


@pytest.fixture
def website(db_ready):
    return factories.WebsiteFactory()


@pytest.fixture
def btbeacon(db_ready):
    return factories.BTBeaconFactory()
