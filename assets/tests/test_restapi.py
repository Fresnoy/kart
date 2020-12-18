from django.test import TestCase
from django.urls import reverse

from assets.models import Gallery


class GalleryEndPoint(TestCase):
    """
    Tests concernants le endpoint des Student
    """
    def setUp(self):
        self.gallery = Gallery(label="Diptyque Marilyn",
                               description="Andrew Warhol's Artwork pictures",)
        self.gallery.save()

    def tearDown(self):
        pass

    def test_list(self):
        """
        Test list of artist
        """
        url = reverse('gallery-list')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    def test_ressource(self):
        """
        Test list of artist
        """
        url = reverse('gallery-detail', kwargs={'pk': 1})
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)
