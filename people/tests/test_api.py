import pytest

from common.tests.conftest import *  # noqa
from diffusion.tests.conftest import *  # noqa
from production.tests.conftest import *  # noqa
from utils.tests.utils import HelpTestForReadOnlyModelRessource, parametrize_user_roles

from .. import api


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestUserRessource(HelpTestForReadOnlyModelRessource):
    resource = api.UserResource

    fixtures = ['user', 'profile']

    expected_list_size = 2
    expected_fields = ['first_name']

    def target(self):
        return self.user

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestUserProfileRessource(TestUserRessource):
    fixtures = ['profile']

    expected_list_size = 1
    expected_fields = ['first_name', 'nationality']

    def target(self):
        return self.profile.user

    def requestor(self):
        return self.profile.user


@pytest.mark.django_db
class TestArtistRessource(HelpTestForReadOnlyModelRessource):
    resource = api.ArtistResource

    fixtures = ['artist', 'artist_profile', 'artist_website', 'artwork']

    expected_list_size = 1
    expected_fields = ['nickname', 'artworks', 'websites']

    post_fields = ['user']
    hyperlinked_fields = {'user': 'people/user'}

    def target(self):
        return self.artist

    def requestor(self):
        return self.artist.user


@pytest.mark.django_db
class TestStaffRessource(HelpTestForReadOnlyModelRessource):
    resource = api.StaffResource

    fixtures = ['staff', 'staff_profile']

    expected_list_size = 1
    expected_fields = ['user']

    post_fields = ['user']
    hyperlinked_fields = {'user': 'people/user'}

    def target(self):
        return self.staff

    def requestor(self):
        return self.staff.user


@pytest.mark.django_db
class TestOrganizationRessource(HelpTestForReadOnlyModelRessource):
    resource = api.OrganizationResource

    fixtures = ['organization', 'place', 'user']

    expected_list_size = 2
    expected_fields = ['name']

    def target(self):
        return self.organization

    def requestor(self):
        return self.user
