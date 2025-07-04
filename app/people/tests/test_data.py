from django.contrib.auth.models import Group
from django.test import TestCase


class GroupData(TestCase):
    """
    Tests concernants les donnees des groupes
    """

    fixtures = ['people/fixtures/groups.json']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fixture(self):
        """
        Test list of user
        """
        group = Group.objects.get(name='School Application')
        assert group.pk > 0
