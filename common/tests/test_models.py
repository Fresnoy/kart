# -*- encoding: utf-8 -*-
from django.test import TestCase
from common.models import Website

from .factories import WebsiteFactory


class CommandsTestCase(TestCase):
    """
        Tests Common Commands
    """

    def setUp(self):
        # create place
        self.website = WebsiteFactory()

    def tearDown(self):
        pass

    def test_websites(self):
        "simple TEST website"
        # get gallery
        website = Website.objects.all()
        # test metaEvent created
        self.assertEqual(website.count(), 1)

    def test_websites_str(self):
        assert self.website.url in str(self.website)
        assert '...' in str(self.website), self.title_fr
        self.website.title_fr = "Andy's website"
        self.website.save()
        assert self.website.title_fr in str(self.website)
        assert '...' not in str(self.website), self.title_fr
        assert self.website.url in str(self.website)
