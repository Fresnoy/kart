# -*- encoding: utf-8 -*-
from django.test import TestCase
from assets.models import Gallery


class CommandsTestCase(TestCase):
    """
        Tests Assets Commands
    """

    def setUp(self):
        # create place
        self.gallery = Gallery(label="Diptyque Marilyn",
                               description="Andrew Warhol's Artwork pictures",)
        self.gallery.save()

    def tearDown(self):
        pass

    def test_gallery(self):
        "simple TEST gallery"
        # get gallery
        galleries = Gallery.objects.all()
        # test metaEvent created
        self.assertEqual(galleries.count(), 1)
