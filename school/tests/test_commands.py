# -*- encoding: utf-8 -*-
from django.core.management import call_command
from io import StringIO
from django.test import TestCase

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from school.tests.factories import StudentApplicationSetupFactory, AdminStudentApplicationFactory


class CommandsTestCase(TestCase):
    """
    Tests School Commands
    """

    def setUp(self):
        self.out = StringIO()

    def tearDown(self):
        pass

    def test_clean_candidatures(self):
        "Test Clean candidature (script for GRPD)."
        self.assertTrue

    def test_application_end_date_reminder(self):
        "Test app end date reminder."
        call_command("application_end_date_reminder", novalidation=True, stdout=self.out)
        self.assertTrue

    def test_application_verify_send_email_templates(self):
        "Test app end date reminder."
        StudentApplicationSetupFactory()
        call_command("application_verify_send_email_templates", stdout=self.out)
        self.assertTrue

    def test_export_selected_applications(self):
        "Test export application selected."
        AdminStudentApplicationFactory()
        call_command("export_selected_applications", dry_run=True, stdout=self.out)
        self.assertTrue

    def test_import_applications(self):
        "Test import applications."
        with File(file=NamedTemporaryFile()) as csvfile:
            csvfile.write(b'test')
            csvfile.write(b'test')
            csvfile.flush()
            call_command("import_applications", input=csvfile.name, mediasurl="http://localhost:8000", stdout=self.out)
            self.assertTrue

    def test_assign_selected_candidatures_to_promo(self):
        "Test assign selected candidature to promo."
        admin_app = AdminStudentApplicationFactory()
        call_command(
            "assign_selected_candidatures_to_promo",
            campaign_id=admin_app.application.campaign.id,
            novalidation=True,
            stdout=self.out,
        )
        self.assertTrue
