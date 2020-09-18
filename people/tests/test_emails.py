import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from school.models import StudentApplicationSetup

from django.test import TestCase
from django.urls import reverse

from django.test.client import RequestFactory

from people.utils import send_activation_email, send_account_information_email


class SendSendEmail(TestCase):
    """
    Tests concernants le endpoint des User
    """
    fixtures = ['groups.json']

    def setUp(self):
        self.user = User()
        self.user.first_name = "Andrew"
        self.user.last_name = "Warhola"
        self.user.username = "awarhol"
        self.user.email = "awarhola@pop.art"
        self.user.save()

        self.setup = StudentApplicationSetup(candidature_date_start=timezone.now() - datetime.timedelta(days=1),
                                             candidature_date_end=timezone.now() + datetime.timedelta(days=1),
                                             recover_password_url="",
                                             authentification_url="",
                                             is_current_setup=True)
        self.setup.save()

    def tearDown(self):
        pass

    def test_email_activation(self):
        """
        Test creat send an activation email
        """
        url = reverse('user-register')
        request = RequestFactory().request(user=url, methods="POST")
        mail_sent = send_activation_email(request, self.user)
        self.assertEqual(mail_sent, True)

    def test_email_account_information(self):
        """
        Test creat send an activation email
        """
        mail_sent = send_account_information_email(self.user)
        self.assertEqual(mail_sent, True)
