import pytest


@pytest.mark.django_db
class TestFresnoyProfile:
    def test_str(self, profile):
        assert str(profile.user) in str(profile)

    def test_is_not_artist(self, profile):
        assert not profile.is_artist

    def test_is_artist(self, artist_profile):
        assert artist_profile.is_artist

    def test_is_not_staff(self, profile):
        assert not profile.is_staff()

    def test_is_staff(self, staff_profile):
        assert staff_profile.is_staff()


@pytest.mark.django_db
class TestArtist:
    def test_str(self, artist):
        assert artist.nickname == str(artist)

    def test_str_without_nickname(self, artist):
        artist.nickname = ""
        artist.save()
        artist_str = str(artist)
        assert artist.user.first_name in artist_str
        assert artist.user.last_name in artist_str


@pytest.mark.django_db
class TestStaff:
    def test_str(self, staff):
        assert str(staff.user) == str(staff)


@pytest.mark.django_db
class TestOrganization:
    def test_str(self, organization):
        assert str(organization.name) == str(organization)
