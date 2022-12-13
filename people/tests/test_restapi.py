from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from people.models import FresnoyProfile
from utils.tests.factories import UserFactory

from .factories import ArtistFactory


class UserEndPoint(TestCase):
    """
    Tests concernants le endpoint des User
    """

    def setUp(self):
        self.user = UserFactory()

        profile = FresnoyProfile(user=self.user)
        profile.save()

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
        url = reverse('rest_register')
        user_registration = {'username': 'newuser', 'email': 'newuser@ac.art',
                             'password1': 'zc7h88', 'password2': 'zc7h88'}
        response = self.client.post(url, user_registration)
        self.assertEqual(response.status_code, 201)
        user_on_base = User.objects.get(email=user_registration.get('email'),
                                        username=user_registration.get('username'))
        assert user_on_base.pk > 0

    def test_user_exist(self):
        """
        Test user exist endpoint
        """
        url = reverse('user-list')
        search = {'user': 'awarhol'}
        response = self.client.get(url, search)
        self.assertEqual(response.status_code, 200)

    def test_patch_user_infos(self):
        """
        Test PATCH user info
        """
        client_auth = APIClient()
        client_auth.force_authenticate(user=self.user)

        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        # send a part of info - must have profile on patch
        info = {'first_name': "Andy", "profile": {"id": self.user.profile.id}}
        response = client_auth.patch(url, data=info, format='json')
        # update ok
        self.assertEqual(response.status_code, 200)
        # info maj
        response = client_auth.get(url)
        self.assertEqual(response.data['first_name'], "Andy")

    def test_put_user_infos(self):
        """
        Test PUT user info
        """
        client_auth = APIClient()
        client_auth.force_authenticate(user=self.user)

        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        # PUT : must send All info
        user_data = client_auth.get(url).data
        # set new name
        user_data['first_name'] = "Andy"
        # Put request
        response = client_auth.put(url, data=user_data, format='json')
        # test update ok
        self.assertEqual(response.status_code, 200)
        response = client_auth.get(url)
        # test info maj
        self.assertEqual(response.data['first_name'], "Andy")


class ArtistEndPoint(TestCase):
    """
    Tests Artist's endpoint
    """
    def setUp(self):
        self.artist = ArtistFactory()

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
