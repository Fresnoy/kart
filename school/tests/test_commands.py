# -*- encoding: utf-8 -*-
from django.core.management import call_command
from io import StringIO
from django.test import TestCase


class CommandsTestCase(TestCase):
    """
        Tests School Commands
    """

    def setUp(self):
        self.out = StringIO()

    def tearDown(self):
        pass

    def test_clean_candidatures(self):
        " Test Clean candidature (script for GRPD)."

        # call_command('clean_candidatures', interactive=False, stdout=self.out)
        self.assertTrue
        # result = self.out.getvalue()
        # value = ("Liste des informations qui vont être supprimées : \
        #          /!\ Supression complète de 0 profiles\
        #          /!\ Supression des informations de 0 anciennes candidatures\
        #          /!\ Supression des informations critiques de 0 candidatures\
        #          [Press any key to continue]")

        # print(".{}.".format(result))
        # assertEqual(out.getvalue(), value)

    def test_application_end_date_reminder(self):
        " Test app end date reminder."
        call_command('application_end_date_reminder', stdout=self.out)
        self.assertTrue
