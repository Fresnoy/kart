import pytest

from . import factories


@pytest.fixture
def promotion(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.PromotionFactory()


@pytest.fixture
def student(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.StudentFactory()


@pytest.fixture
def student_application_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.StudentApplicationSetupFactory()


@pytest.fixture
def student_application(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return factories.StudentApplicationFactory()
