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
