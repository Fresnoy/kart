from django.contrib.auth.models import User

from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Artist


class UserEndPoint(TestCase):
    """
    Tests concernants le endpoint des User
    """
    def setUp(self):
        self.user = User()
        self.user.first_name = "Andrew"
        self.user.last_name = "Warhola"
        self.user.username = "awarhol"
        self.user.save()

        self.response = None

    def tearDown(self):
        self.response = None

    def test_list(self):
        """
        Test list of user
        """
        url = reverse('user-list')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)


class ArtistEndPoint(TestCase):
    """
    Tests concernants le endpoint des Student
    """
    def setUp(self):
        self.user = User()
        self.user.first_name = "Andrew"
        self.user.last_name = "Warhola"
        self.user.username = "awarhol"
        self.user.save()

        self.artist = Artist(user=self.user, nickname="Andy Warhol")
        self.artist.save()

        self.response = None

    def tearDown(self):
        self.response = None

    def test_list(self):
        """
        Test list of artist
        """
        url = reverse('artist-list')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)
