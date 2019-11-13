# -*- encoding: utf-8 -*-
from django.test import TestCase
from common.models import Website


class CommandsTestCase(TestCase):
    """
        Tests Common Commands
    """

    def setUp(self):
        # create place
        self.website = Website(title_fr="Site web d'Andy Warhol",
                               title_en="Andrew Warhol's Website",
                               language="EN",
                               url="https://www.warhol.org/",)
        self.website.save()

    def tearDown(self):
        pass

    def test_websites(self):
        "simple TEST website"
        # get gallery
        website = Website.objects.all()
        # test metaEvent created
        self.assertEqual(website.count(), 1)
