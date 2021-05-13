import pytest


@pytest.mark.django_db
class TestWebsite:
    def test_str(self, website):
        website_str = str(website)
        assert website.url in website_str
        assert '...' in website_str or len(website.title_fr) <= 20

    def test_short_str(self, website):
        website.title_fr = "Andy's website"
        website.save()
        website_str = str(website)
        assert website.title_fr in website_str
        assert '...' not in website_str
        assert website.url in website_str


@pytest.mark.django_db
class TestBTBeacon:
    def test_BTBeacon_str(self, btbeacon):
        btbeacon_str = str(btbeacon)
        assert btbeacon.label in btbeacon_str
        assert str(btbeacon.uuid) in btbeacon_str
