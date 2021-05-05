import io
from django.test import TestCase
from django.urls import reverse

from PIL import Image

from rest_framework.test import APIClient

from assets.models import Gallery, Medium
from utils.tests.factories import SuperAndyFactory


class GalleryEndPoint(TestCase):
    """
    Tests concernants Gallery's endpoint
    """
    def setUp(self):
        self.user = SuperAndyFactory()

        self.gallery = Gallery(label="Diptyque Marilyn",
                               description="Andrew Warhol's Artwork pictures",)
        self.gallery.save()

    def tearDown(self):
        pass

    def test_list(self):
        """
        Test list of gallery endpoint
        """
        url = reverse('gallery-list')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    def test_ressource(self):
        """
        Test acces detail of gallery endpoint
        """
        url = reverse('gallery-detail', kwargs={'pk': 1})
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    def test_create_gallery(self):
        """
        Test create gallery endpoint
        """

        self.client_auth = APIClient()
        self.client_auth.force_authenticate(user=self.user)

        url = reverse('gallery-list')
        data = {
            'label': 'test',
            'description': 'test'}
        self.response = self.client_auth.post(url, data)
        self.assertEqual(self.response.status_code, 201)


class MediumEndPoint(TestCase):
    """
    Tests concernants Medium's endpoint
    """
    def setUp(self):
        # User
        self.user = SuperAndyFactory()

        self.client_auth = APIClient()
        self.client_auth.force_authenticate(user=self.user)
        # Gallery
        self.gallery = Gallery(label="Diptyque Marilyn",
                               description="Andrew Warhol's Artwork pictures",)
        self.gallery.save()
        # Medium
        self.medium = Medium(label="Picture Diptyque Marilyn",
                             description="Color & Grey Marilyn",
                             gallery=self.gallery,)
        self.medium.save()

    def tearDown(self):
        pass

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_list(self):
        """
        Test list of medium
        """
        url = reverse('medium-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_ressource(self):
        """
        Test detail of media
        """
        url = reverse('medium-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_upload_image(self):
        """
        Test upload file
        """
        self.client_auth.force_authenticate(user=self.user)
        url_post_media = reverse('medium-detail', kwargs={'pk': 1})
        file = self.generate_photo_file()
        data = {
            'label': 'Upload',
            'description': 'test',
            'gallery': reverse('gallery-detail', kwargs={'pk': self.gallery.id}),
            'picture': file,
        }
        response = self.client_auth.patch(url_post_media, data=data)
        assert response.status_code == 200
