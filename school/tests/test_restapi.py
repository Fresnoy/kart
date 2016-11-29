import json

from django.contrib.auth.models import User

from django.test import TestCase
from django.core.urlresolvers import reverse

from people.models import Artist

from ..models import StudentApplication


class TestApplicationEndPoint(TestCase):
    """
    Tests concernants le endpoint des Student Application
    """

    def setUp(self):
        self.user = User()
        self.user.first_name = "Andrew"
        self.user.last_name = "Warhola"
        self.user.username = "awarhol"
        self.user.save()

        self.artist = Artist(user=self.user, nickname="Andy Warhol")
        self.artist.save()

        self.application = StudentApplication(artist=self.artist)
        self.application.save()

        self.response = None

    def tearDown(self):
        self.response = None

    def test_list(self):
        """
        Test list of applications
        """

        url = reverse('studentapplication-list')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    def test_json_response(self):
        """
        Test JSON response
        """
        self.test_list()
        self.assertTrue(json.loads(self.response.content))

    def test_first_app_default_value(self):
        """
        Test default value
        """
        url = reverse('studentapplication-detail', kwargs={'pk': 1})
        self.response = self.client.get(url)
        self.assertEqual(self.response.data['first_time'], True)

    def test_list_contain_artist(self):
        """
        informations tests
        """
        self.test_list()
        urlartist = reverse('artist-detail', kwargs={'pk': 1})
        self.assertContains(self.response, urlartist)
