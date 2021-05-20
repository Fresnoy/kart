import pytest

from utils.tests.conftest import *  # noqa

from . import factories


@pytest.fixture
def gallery(db_ready):
    return factories.GalleryFactory()


@pytest.fixture
def medium(db_ready):
    return factories.MediumFactory()
