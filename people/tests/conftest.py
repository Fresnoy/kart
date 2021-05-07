import pytest

from . import factories


@pytest.fixture
def artist(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.ArtistFactory()
