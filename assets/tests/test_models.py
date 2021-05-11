import pytest


@pytest.mark.django_db
class TestGalery:
    def test_str(self, gallery):
        gallery_str = str(gallery)
        assert gallery.label in gallery_str
        assert gallery.description in gallery_str


@pytest.mark.django_db
class TestMedium:
    def test_str(self, medium):
        medium_str = str(medium)
        assert medium.label in medium_str
        assert medium.description in medium_str
