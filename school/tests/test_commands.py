# -*- encoding: utf-8 -*-
from django.core.management import call_command
from io import StringIO
from django.test import TestCase
from school.tests.factories import StudentApplicationSetupFactory


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
        self.assertTrue

    def test_application_end_date_reminder(self):
        " Test app end date reminder."
        call_command('application_end_date_reminder', stdout=self.out)
        self.assertTrue

    def test_application_verify_send_email_templates(self):
        " Test app end date reminder."
        StudentApplicationSetupFactory()
        call_command('application_verify_send_email_templates', stdout=self.out)
        self.assertTrue
