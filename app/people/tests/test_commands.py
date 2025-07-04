import factory

from django.core.management import call_command
from io import StringIO
from django.test import TestCase

from people.models import Staff


class CommandsTestCase(TestCase):
    """
        Tests Diffusion Commands
    """

    def setUp(self):
        # init command output
        self.out = StringIO()
        pass

    def tearDown(self):
        pass

    def test_create_staff(self):
        "simple TEST Command: create_staff"
        call_command('create_staff', factory.Faker('first_name'), factory.Faker('name'),
                     stdout=self.out)
        place = Staff.objects.all()
        self.assertEqual(place.count(), 1)
