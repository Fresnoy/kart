import pytest

from .factories import ArtistFactory, FresnoyProfileFactory, OrganizationFactory, StaffFactory


@pytest.mark.django_db
class TestFresnoyProfile:
    def setup(self):
        self.profile = FresnoyProfileFactory()

    def test_str(self):
        assert str(self.profile.user) in str(self.profile)

    def test_is_not_artist(self):
        assert not self.profile.is_artist

    def test_is_artist(self):
        self.profile = FresnoyProfileFactory(user=ArtistFactory().user)
        assert self.profile.is_artist

    def test_is_not_staff(self):
        assert not self.profile.is_staff()

    def test_is_staff(self):
        self.profile = FresnoyProfileFactory(user=StaffFactory().user)
        assert self.profile.is_staff()


@pytest.mark.django_db
class TestArtist:
    def setup(self):
        self.artist = ArtistFactory()

    def test_str(self):
        assert self.artist.nickname == str(self.artist)

    def test_str_without_nickname(self):
        self.artist.nickname = None
        assert str(self.artist.user) in str(self.artist)


@pytest.mark.django_db
class TestStaff:
    def setup(self):
        self.staff = StaffFactory()

    def test_str(self):
        assert str(self.staff.user) == str(self.staff)


@pytest.mark.django_db
class TestOrganization:
    def setup(self):
        self.organization = OrganizationFactory()

    def test_str(self):
        assert str(self.organization.name) == str(self.organization)
