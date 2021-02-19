import datetime
from django.test.client import RequestFactory
from django.utils import timezone
from django.contrib.auth.models import User

from school.models import StudentApplication, StudentApplicationSetup, Promotion

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from people.models import Artist

from school.utils import (send_candidature_completed_email_to_user,
                          send_candidature_completed_email_to_admin,
                          send_candidature_complete_email_to_candidat,
                          send_interview_selection_email_to_candidat,
                          send_not_selected_email_to_candidat,
                          )


class SendSendEmail(TestCase):
    """
    Tests concernants le endpoint des User
    """
    fixtures = ['groups.json']

    def setUp(self):
        self.user = User(first_name="Andrew",
                         last_name="Warhola",
                         username="awarhol",
                         email="awarhola@pop.art")
        self.user.save()
        # force authenticate
        self.client_auth = APIClient()
        self.client_auth.force_authenticate(user=self.user)

        self.artist = Artist(user=self.user, nickname="Andy Warhol")
        self.artist.save()

        self.promotion = Promotion(name="Promo", starting_year=timezone.now().year, ending_year=timezone.now().year+1)
        self.promotion.save()

        self.campaign = StudentApplicationSetup(candidature_date_start=timezone.now(),
                                                candidature_date_end=timezone.now() + datetime.timedelta(days=1),
                                                interviews_start_date=timezone.now() + datetime.timedelta(days=2),
                                                interviews_end_date=timezone.now() + datetime.timedelta(days=3),
                                                is_current_setup=True,
                                                promotion=self.promotion)
        self.campaign.save()
        # add a candidature
        self.application = StudentApplication(artist=self.artist,
                                              campaign=self.campaign,
                                              interview_date=timezone.now() + datetime.timedelta(days=2, hours=3),)
        self.application.save()
        #
        self.studentapplication_detail_url = reverse('studentapplication-detail', kwargs={'pk': self.application.pk})

    def tearDown(self):
        pass

    def test_email_candidature_completed_to_user(self):
        """
        Test send an candidature completed email to user
        """
        request = RequestFactory().request(url=self.studentapplication_detail_url, methods="PATCH")
        mail_sent = send_candidature_completed_email_to_user(request, self.user, self.application)
        self.assertEqual(mail_sent, True)

    def test_email_candidature_completed_to_admin(self):
        """
        Test send an candidature completed email to admin
        """
        request = RequestFactory().request(url=self.studentapplication_detail_url, methods="PATCH")
        mail_sent = send_candidature_completed_email_to_admin(request, self.user, self.application)
        self.assertEqual(mail_sent, True)

    def test_email_candidature_complete_to_candidat(self):
        """
        Test send an candidature complete email to user
        """
        request = RequestFactory().request(url=self.studentapplication_detail_url, methods="PATCH")
        mail_sent = send_candidature_complete_email_to_candidat(request, self.user, self.application)
        self.assertEqual(mail_sent, True)

    def test_email_interview_selection_to_candidat(self):
        """
        Test send an interveiw selection email to user
        """
        request = RequestFactory().request(url=self.studentapplication_detail_url, methods="PATCH")
        mail_sent = send_interview_selection_email_to_candidat(request, self.user, self.application)
        self.assertEqual(mail_sent, True)

    def test_send_not_selected_email_to_candidat(self):
        """
        Test send an not selected to user
        """
        request = RequestFactory().request(url=self.studentapplication_detail_url, methods="PATCH")
        mail_sent = send_not_selected_email_to_candidat(request, self.user, self.application)
        print(mail_sent)
        self.assertEqual(mail_sent, True)
