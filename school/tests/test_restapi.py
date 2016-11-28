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
        self.user.first_name = "Me"
        self.user.last_name = "Loo"
        self.user.username = "Tintin"
        self.user.save()

        self.artist = Artist(user = self.user, nickname="Rintintin")
        self.artist.save()

        self.application = StudentApplication(artist = self.artist)
        self.application.save()


    def tearDown(self):
        pass


    def test_list(self):
        """
        Test list of applications
        """

        url = reverse('studentapplication-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_list_contain_user(self):
        """
        informations tests
        """
        # TODO le test

        pass
