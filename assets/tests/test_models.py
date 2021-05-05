# -*- encoding: utf-8 -*-
from django.test import TestCase
from assets.models import Gallery, Medium

from .factories import MediumFactory


class ModelsTestCase(TestCase):
    """
        Tests Assets Models
    """

    def setUp(self):
        # create place
        self.medium = MediumFactory()

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
