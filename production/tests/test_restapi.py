
from django.test import TestCase

from django.urls import reverse
from .factories import TagFactory


class KeywordsEndPoint(TestCase):
    """
    Tests concernants le endpoint des User
    """

    def setUp(self):
        self.keyword = TagFactory()

    def tearDown(self):
        pass

    def test_list(self):
        """
        Test list of user
        """
        url = reverse('tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ArtworkSearchEndPoint(TestCase):
    """
    Tests Artwork Search endpoint
    TODO: Dont find how test with elasticseach/drf-haystack <-> test env
          => elasticsearch doesnt have acces to the env test
    """
    def test_pagination(self):
        """
        Paging improves result response time
        """
        pass

    def test_result_fields(self):
        """
        Test field by artwork search endpoint
        Must have 'title', 'url', 'type', 'genres', 'keywords', "shooting_place", "authors"
        """
        pass
