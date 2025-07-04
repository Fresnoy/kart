import pytest

from people.tests.conftest import *  # noqa
from utils.tests.conftest import *  # noqa

from . import factories


@pytest.fixture
def website(db_ready):
    return factories.WebsiteFactory()


@pytest.fixture
def artist_website(db_ready, artist):
    website = factories.WebsiteFactory()
    artist.websites.add(website)
    return website


@pytest.fixture
def btbeacon(db_ready):
    return factories.BTBeaconFactory()
