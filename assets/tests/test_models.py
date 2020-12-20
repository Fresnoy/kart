# -*- encoding: utf-8 -*-
from django.test import TestCase
from assets.models import Gallery, Medium


class ModelsTestCase(TestCase):
    """
        Tests Assets Models
    """

    def setUp(self):
        # create place
        self.gallery = Gallery(label="Diptyque Marilyn",
                               description="Andrew Warhol's Artwork pictures",)
        self.gallery.save()

        self.medium = Medium(label="Picture Diptyque Marilyn",
                             description="Color & Grey Marilyn",
                             gallery=self.gallery,)
        self.medium.save()

    def tearDown(self):
        pass

    def test_gallery(self):
        "simple TEST gallery"
        # get gallery
        galleries = Gallery.objects.all()
        # test gallerie created
        self.assertEqual(galleries.count(), 1)

    def test_medium(self):
        "simple TEST medium"
        # get gallery
        media = Medium.objects.all()
        # test medium created
        self.assertEqual(media.count(), 1)
