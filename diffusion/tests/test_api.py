import pytest

from common.tests.conftest import *  # noqa
from production.tests.conftest import *  # noqa
from utils.tests.utils import HelpTestForReadOnlyModelRessource

from .. import api


@pytest.mark.django_db
class TestPlaceRessource(HelpTestForReadOnlyModelRessource):
    model = api.PlaceResource

    fixtures = ['user', 'place']

    expected_list_size = 1
    expected_fields = ['name', 'latitude', 'longitude']

    def target(self):
        return self.place

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestAwardRessource(HelpTestForReadOnlyModelRessource):
    model = api.AwardResource

    fixtures = ['award', 'artist', 'artwork']

    expected_list_size = 1
    expected_fields = ['date', 'meta_award', 'artwork', 'artist']

    def target(self):
        return self.award

    def requestor(self):
        return self.artist.user


@pytest.mark.django_db
class TestMetaAwardRessource(HelpTestForReadOnlyModelRessource):
    model = api.MetaAwardResource

    fixtures = ['meta_award', 'user']

    expected_list_size = 1
    expected_fields = ['label', 'event', 'task']

    def target(self):
        return self.meta_award

    def requestor(self):
        return self.user
