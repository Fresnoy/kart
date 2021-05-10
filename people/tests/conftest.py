import pytest

from . import factories


@pytest.fixture
def profile(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.FresnoyProfileFactory()


@pytest.fixture
def artist(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.ArtistFactory()


@pytest.fixture
def andy(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.ArtistFactory(nickname="Andy Warhol")


@pytest.fixture
def artist_profile(django_db_setup, django_db_blocker, artist):
    with django_db_blocker.unblock():
        return factories.FresnoyProfileFactory(user=artist.user)


@pytest.fixture
def staff(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.StaffFactory()


@pytest.fixture
def staff_profile(django_db_setup, django_db_blocker, staff):
    with django_db_blocker.unblock():
        return factories.FresnoyProfileFactory(user=staff.user)


@pytest.fixture
def organization(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.OrganizationFactory()
