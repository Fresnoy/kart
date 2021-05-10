import pytest

from . import factories


@pytest.fixture
def gallery(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.GalleryFactory()


@pytest.fixture
def medium(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.MediumFactory()
