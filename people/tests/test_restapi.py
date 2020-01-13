from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse

from people.models import Artist


class UserEndPoint(TestCase):
    """
    Tests concernants le endpoint des User
    """
    fixtures = ['groups.json']

    def setUp(self):
        self.user = User()
        self.user.first_name = "Andrew"
        self.user.last_name = "Warhola"
        self.user.username = "awarhol"
        self.user.save()

    def tearDown(self):
        pass

    def _get_list(self):
        url = reverse('user-list')
        return self.client.get(url)

    def test_list(self):
        """
        Test list of user
        """
        response = self._get_list()
        self.assertEqual(response.status_code, 200)

    def test_user_register(self):
        """
        Test user register link
        """
        url = reverse('user-register')
        user_registration = {'username': 'newuser', 'first_name': 'New', 'last_name': 'User', 'email': 'newuser@ac.art'}
        response = self.client.post(url, user_registration)
        self.assertEqual(response.status_code, 202)
        user_on_base = User.objects.get(email=user_registration.get('email'),
                                        first_name=user_registration.get('first_name'),
                                        last_name=user_registration.get('last_name'),
                                        username=user_registration.get('username'))
        assert user_on_base.pk > 0
        assert user_on_base.profile is not None

    def test_user_exist(self):
        """
        Test user exist endpoint
        """
        url = reverse('user-list')
        search = {'user': 'awarhol'}
        response = self.client.get(url, search)
        self.assertEqual(response.status_code, 200)


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
