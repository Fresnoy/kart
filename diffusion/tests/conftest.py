import pytest

from . import factories


@pytest.fixture
def place(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.PlaceFactory()


@pytest.fixture
def meta_award(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.MetaAwardFactory()


@pytest.fixture
def award(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.AwardFactory()


@pytest.fixture
def meta_event(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.MetaEventFactory()


@pytest.fixture
def diffusion(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.DiffusionFactory()
