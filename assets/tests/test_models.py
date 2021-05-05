import pytest

from assets.models import Gallery, Medium

from .factories import MediumFactory


@pytest.mark.django_db
class TestModels:
    """
        Tests Assets Models
    """
    def setup(self):
        self.medium = MediumFactory()

    def test_gallery(self):
        galleries = Gallery.objects.all()
        assert galleries.count() == 1

    def test_gallery_str(self):
        assert self.medium.gallery.label in str(self.medium.gallery)
        assert self.medium.gallery.description in str(self.medium.gallery)

    def test_medium(self):
        media = Medium.objects.all()
        assert media.count() == 1

    def test_medium_str(self):
        assert self.medium.label in str(self.medium)
        assert self.medium.description in str(self.medium)
