import pytest

from utils.tests.conftest import *  # noqa

from . import factories


@pytest.fixture
def profile(db_ready):
    return factories.FresnoyProfileFactory()


@pytest.fixture
def artist(db_ready):
    return factories.ArtistFactory()


@pytest.fixture
def andy(db_ready):
    return factories.ArtistFactory(nickname="Andy Warhol")


@pytest.fixture
def artist_profile(db_ready, artist):
    return factories.FresnoyProfileFactory(user=artist.user)


@pytest.fixture
def staff(db_ready):
    return factories.StaffFactory()


@pytest.fixture
def staff_profile(db_ready, staff):
    return factories.FresnoyProfileFactory(user=staff.user)


@pytest.fixture
def organization(db_ready):
    return factories.OrganizationFactory()
