import pytest


@pytest.fixture
def db_ready(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock() as db:
        return db
