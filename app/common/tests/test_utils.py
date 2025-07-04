# -*- encoding: utf-8 -*-
import os

from django.core.files import File
from django.test import TestCase
from io import BytesIO

from PIL import Image

from django.conf import settings

from assets.tests.factories import MediumFactory


def create_image(filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the data.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    return File(data, name=filename)


class UploadTestCase(TestCase):
    """
        Tests Upload Commands
    """

    def setUp(self):
        self.medium = MediumFactory()

    def tearDown(self):
        pass

    def test_upload_file_image(self):
        "simple TEST upload"
        # set up file name
        image_name = '#éavatar!$*'
        image_name_slug = 'avatar'
        # create image file
        image_file = create_image(image_name+'.png')
        # set to medium
        self.medium.picture = image_file
        self.medium.save()
        # tests
        # contain the name of the file
        self.assertIn(image_name_slug, self.medium.picture.name)
        # name without accent
        self.assertNotIn(image_name[1], self.medium.picture.name)
        # name without root path
        self.assertNotIn(settings.MEDIA_ROOT.replace(os.sep, '/'), self.medium.picture.name)
        # media url with url settings
        self.assertIn(settings.MEDIA_URL, self.medium.picture.url)
        # media path with root settings
        self.assertIn(settings.MEDIA_ROOT, self.medium.picture.path)
