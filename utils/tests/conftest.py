import pytest

from . import factories


@pytest.fixture
def db_ready(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock() as db:
        return db


@pytest.fixture
def user(db_ready):
    return factories.UserFactory()


@pytest.fixture
def inactive_user(db_ready):
    return factories.UserFactory(is_active=False)


@pytest.fixture
def admin(db_ready):
    return factories.AdminFactory()


@pytest.fixture
def joker(db_ready):
    # return a user-like object nonexistant in db
    return factories.UserFactory.stub()
