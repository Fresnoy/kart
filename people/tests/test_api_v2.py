import pytest

from common.tests.conftest import *  # noqa
from diffusion.tests.conftest import *  # noqa
from production.tests.conftest import *  # noqa
from utils.tests.utils import (
    IsAuthenticatedOrReadOnlyModelViewSetMixin,
    HelpTestForModelViewSet,
    parametrize_user_roles,
)


def pytest_generate_tests(metafunc):
    # pytest hook; called once per each test function
    parametrize_user_roles(metafunc)


@pytest.mark.django_db
class TestUserViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'people/user'

    fixtures = ['user', 'profile']

    expected_list_size = 2
    expected_fields = ['first_name']

    mutate_fields = ['username']
    put_fields = ['username', 'last_name', 'first_name']

    def target(self):
        return self.user

    def requestor(self):
        return self.user


@pytest.mark.django_db
class TestPrivateUserProfileViewSet(TestUserViewSet):
    fixtures = ['profile']

    expected_list_size = 1
    expected_fields = ['first_name', 'profile__nationality']

    _user_roles = ['user', 'jwt']

    methods_behavior = {
        # list not tested since it only expose TestUserViewSet.expected_fields
        'get': 200,
        'patch': 200,
        'put': 200,
        'post': 405,
        'delete': 204,
    }

    def target(self):
        return self.profile.user

    def requestor(self):
        return self.profile.user


@pytest.mark.django_db
class TestProfileViewSet(HelpTestForModelViewSet):
    viewset_name = 'people/userprofile'
    fixtures = ['profile']

    expected_list_size = 1
    expected_fields = ['birthdate', 'nationality']

    mutate_fields = ['nationality']
    put_fields = ['nationality']

    def target(self):
        return self.profile

    def requestor(self):
        return self.profile.user


@pytest.mark.django_db
class TestArtistViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'people/artist'

    fixtures = ['artist', 'artist_profile', 'artist_website', 'artwork']

    expected_list_size = 1
    expected_fields = ['nickname', 'bio_short_fr', 'websites']

    mutate_fields = ['nickname']
    put_fields = ['nickname', 'user']
    hyperlinked_fields = {'user': 'user'}

    def target(self):
        return self.artist

    def requestor(self):
        return self.artist.user


@pytest.mark.django_db
class TestStaffViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'people/staff'

    fixtures = ['staff', 'staff_profile']

    expected_list_size = 1
    expected_fields = ['user']

    mutate_fields = ['user']
    put_fields = ['user']
    hyperlinked_fields = {'user': 'user'}

    def target(self):
        return self.staff

    def requestor(self):
        return self.staff.user


@pytest.mark.django_db
class TestOrganizationViewSet(IsAuthenticatedOrReadOnlyModelViewSetMixin, HelpTestForModelViewSet):
    viewset_name = 'people/organization'

    fixtures = ['organization', 'place', 'user']

    expected_list_size = 2
    expected_fields = ['name', 'description']

    mutate_fields = ['name']
    put_fields = ['name', 'description']

    def target(self):
        return self.organization

    def requestor(self):
        return self.user
