import pytest

from common.models import Website

from .factories import BTBeaconFactory, WebsiteFactory


@pytest.mark.django_db
class TestWebsite:
    """
        Tests Common Models
    """
    def setup(self):
        self.website = WebsiteFactory()

    def test_websites(self):
        websites = Website.objects.all()
        assert websites.count() == 1

    def test_websites_str(self):
        assert self.website.url in str(self.website)
        assert '...' in str(self.website), self.title_fr

    def test_websites_short_str(self):
        self.website.title_fr = "Andy's website"
        assert self.website.title_fr in str(self.website)
        assert '...' not in str(self.website), self.title_fr
        assert self.website.url in str(self.website)


@pytest.mark.django_db
class TestBTBeacon:
    def test_BTBeacon_str(self):
        beacon = BTBeaconFactory()
        assert beacon.label in str(beacon)
        assert str(beacon.uuid) in str(beacon)
