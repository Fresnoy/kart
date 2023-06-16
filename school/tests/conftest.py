import pytest

from utils.tests.conftest import *  # noqa

from . import factories


@pytest.fixture
def promotion(db_ready):
    return factories.PromotionFactory()


@pytest.fixture
def student(db_ready):
    return factories.StudentFactory()


@pytest.fixture
def scientificstudent(db_ready):
    return factories.ScientificStudentFactory()


@pytest.fixture
def phdstudent(db_ready):
    return factories.PhdStudentFactory()


@pytest.fixture
def teachingartist(db_ready):
    return factories.TeachingArtistFactory()


@pytest.fixture
def student_application_setup(db_ready, school_application_group):
    return factories.StudentApplicationSetupFactory()


@pytest.fixture
def student_application(db_ready, school_application_group):
    return factories.StudentApplicationFactory()
