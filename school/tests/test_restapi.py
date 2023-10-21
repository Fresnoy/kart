import json
import datetime
# import time
from django.utils import timezone

from django.contrib.auth.models import User, Group, Permission

from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.urls import reverse

from people.models import FresnoyProfile
from people.tests.factories import ArtistFactory
from school.tests.factories import AdminStudentApplicationFactory, StudentApplicationFactory
from school.models import StudentApplication, StudentApplicationSetup, Promotion


class TestApplicationEndPoint(TestCase):
    """
    Tests concernants le endpoint des Student Application
    """
    fixtures = ['people/fixtures/groups.json']

    def setUp(self):
        self.artist = ArtistFactory()
        self.user = self.artist.user
        FresnoyProfile.objects.create(user=self.user)
        self.sa_group = Group.objects.first()
        self.user.groups.add(self.sa_group)
        self.user.save()

        # save generate token
        self.token = ""
        self.client_auth = APIClient()

    def tearDown(self):
        pass

    def _get_list(self):
        url = reverse('studentapplication-list')
        return self.client.get(url)

    def _get_list_auth(self):
        url = reverse('studentapplication-list')
        return self.client_auth.get(url)

    def test_list(self):
        """
        Test list of applications without authentification
        """
        # set up a candidature
        application = StudentApplication(artist=self.artist)
        application.save()

        self.token = ""
        response = self._get_list()
        candidatures = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(candidatures)
        self.assertEqual(len(candidatures), 1)
        # info is NOT accessible when anonymous user
        self.assertRaises(KeyError, lambda: candidatures[0]['current_year_application_count'])

    def test_list_auth(self):
        """
        Test list of applications with authentification
        """
        # set up a candidature
        application = StudentApplication(artist=self.artist)
        application.save()

        self.client_auth.force_authenticate(user=self.user)
        response = self._get_list_auth()
        candidature = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # info is accessible when user is auth
        assert candidature[0]['current_year_application_count'] is not None

    def test_user_register(self):
        """
        Test user register link
        """
        url = reverse('studentapplication-user-register')
        user_registration = {'username': 'newuser', 'first_name': 'New', 'last_name': 'User', 'email': 'newuser@ac.art'}
        response = self.client.post(url, user_registration)
        self.assertEqual(response.status_code, 202)
        user_on_base = User.objects.get(email=user_registration.get('email'),
                                        first_name=user_registration.get('first_name'),
                                        last_name=user_registration.get('last_name'),
                                        username=user_registration.get('username'))
        assert user_on_base.pk > 0
        assert user_on_base.profile is not None

    def test_user_has_createStudentApplication_permission(self):
        """
        Test user permission
        """
        permission = Permission.objects.get(codename='add_studentapplication')
        self.assertEqual(self.user.has_perm(permission.content_type.app_label + '.' + permission.codename), True)

    def test_userWithoutGroup_create_student_application(self):
        """
        Test user without group create an studentapplication
        """
        self.assertEqual(self.user.groups.filter(name=self.sa_group.name).exists(), True)
        # remove user from Group
        self.sa_group.user_set.remove(self.user)
        # test user has no Student Application group
        self.assertEqual(self.user.groups.filter(name=self.sa_group.name).exists(), False)
        # get uri
        studentapplication_url = reverse('studentapplication-list')
        # auth user
        self.client_auth.force_authenticate(user=self.user)
        # post method
        response = self.client_auth.post(studentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_userWithgroup_create_student_application(self):
        """
        Test creating an studentapplication
        """
        self.client_auth.force_authenticate(user=self.user)
        # test if user in group
        self.assertEqual(self.user.groups.filter(name=self.sa_group.name).exists(), True)

        studentapplication_url = reverse('studentapplication-list')
        response = self.client_auth.post(studentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentApplication.objects.count(), 1)
        self.assertEqual(StudentApplication.objects.last().artist.user.first_name, self.user.first_name)

    def test_anonymUser_create_student_application(self):
        """
        Test creating an studentapplication
        """
        studentapplication_url = reverse('studentapplication-list')
        response = self.client_auth.post(studentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # get method (join user in group)
        response = self.client_auth.get(studentapplication_url)
        # post again
        response = self.client_auth.post(studentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_student_application(self):
        """
        Test creating an studentapplication
        """
        # set up a campaign
        promotion = Promotion(starting_year=2000, ending_year=2001)
        promotion.save()
        campaign = StudentApplicationSetup(candidature_date_start=timezone.now(),
                                           candidature_date_end=timezone.now() + datetime.timedelta(days=1),
                                           promotion=promotion,
                                           is_current_setup=True,)
        campaign.save()
        # add a candidature
        application = StudentApplication(artist=self.artist, campaign=campaign)
        application.save()
        # auth user
        self.client_auth.force_authenticate(user=self.user)
        studentapplication_url = reverse('studentapplication-detail', kwargs={'pk': application.pk})
        # update an info
        response = self.client_auth.patch(studentapplication_url,
                                          data={'remote_interview': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_anotherstudent_application(self):
        """
        Test update an studentapplication
        """
        application = StudentApplicationFactory()

        self.client_auth.force_authenticate(user=self.user)
        studentapplication_url = reverse('studentapplication-detail', kwargs={'pk': application.pk})
        # update an info
        response = self.client_auth.patch(studentapplication_url,
                                          data={'remote_interview': 'true'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_birthdate_on_student_application(self):
        """
        Test creating an studentapplication
        """
        # set up a campaign
        promotion = Promotion(starting_year=2000, ending_year=2001)
        promotion.save()
        campaign = StudentApplicationSetup(candidature_date_start=timezone.now(),
                                           candidature_date_end=timezone.now() + datetime.timedelta(days=1),
                                           promotion=promotion,
                                           date_of_birth_max=datetime.date(1983, 12, 31),
                                           is_current_setup=True,)
        campaign.save()
        # add a candidature
        application = StudentApplication(artist=self.artist, campaign=campaign)
        application.save()
        # auth user
        self.client_auth.force_authenticate(user=self.user)
        user_url = reverse('user-detail', kwargs={'pk': self.user.pk})
        # update bad info
        response = self.client_auth.patch(user_url,
                                          data={'profile.birthdate': '1983-12-30'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.user.profile.birthdate, '1983-12-30')
        # update OK info
        response = self.client_auth.patch(user_url,
                                          data={'profile.birthdate': '1983-12-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['birthdate'], '1983-12-31')


class TestApplicationSetupEndPoint(TestCase):
    """
    Tests concernants le endpoint des Student Application Setups
    """
    def setUp(self):
        promotion = Promotion(starting_year=2000, ending_year=2001)
        promotion.save()
        campaign = StudentApplicationSetup(candidature_date_start=timezone.now() - datetime.timedelta(days=1),
                                           candidature_date_end=timezone.now() + datetime.timedelta(days=1),
                                           promotion=promotion,
                                           is_current_setup=True,)
        campaign.save()

        campaign = StudentApplicationSetup(candidature_date_start=timezone.now() - datetime.timedelta(days=2),
                                           candidature_date_end=timezone.now() - datetime.timedelta(days=1),
                                           promotion=promotion,
                                           is_current_setup=False,)
        campaign.save()

    def tearDown(self):
        pass

    def _get_list(self):
        url = reverse('studentapplicationsetup-list')
        return self.client.get(url)

    def _get_current_campaign(self):
        url = reverse('studentapplicationsetup-list')
        return self.client.get("{}?is_current_setup=true".format(url))

    def test_list(self):
        """
        Test list of applications without authentification
        """
        response = self._get_list()
        campaign = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(campaign), 2)

    def test_campaign_open(self):
        """
        Test list of applications without authentification
        """
        response = self._get_current_campaign()
        campaign = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(campaign), 1)
        # info is True
        self.assertTrue(campaign[0]['candidature_open'])


class TestAdminApplicationEndPoint(TestCase):
    """
    Tests concernants le endpoint des Student Application
    """
    fixtures = ['people/fixtures/groups.json']

    def setUp(self):
        self.application_admin = AdminStudentApplicationFactory()

        self.artist = ArtistFactory()
        self.user = self.artist.user
        self.sa_group = Group.objects.first()
        self.user.groups.add(self.sa_group)
        self.user.save()
        self.client_auth = APIClient()

    def tearDown(self):
        pass

    def test_anonymUser_list(self,):
        adminstudentapplication_url = reverse('adminstudentapplication-list')
        response = self.client_auth.post(adminstudentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_candidat_list(self,):
        self.client_auth.force_authenticate(user=self.user)
        # test if user in group
        self.assertEqual(self.user.groups.filter(name=self.sa_group.name).exists(), True)

        adminstudentapplication_url = reverse('adminstudentapplication-list')
        response = self.client_auth.post(adminstudentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_candidat_update(self,):
        self.client_auth.force_authenticate(user=self.user)

        adminstudentapplication_url = reverse('adminstudentapplication-detail',
                                              kwargs={'pk': self.application_admin.pk})
        response = self.client_auth.put(adminstudentapplication_url, data={'selected': 'true'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_list(self,):
        self.user.is_staff = True
        self.client_auth.force_authenticate(user=self.user)

        adminstudentapplication_url = reverse('adminstudentapplication-list')
        response = self.client_auth.get(adminstudentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_create(self,):
        self.user.is_staff = True
        self.client_auth.force_authenticate(user=self.user)

        adminstudentapplication_url = reverse('adminstudentapplication-list')
        response = self.client_auth.post(adminstudentapplication_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_update(self,):
        self.user.is_staff = True
        self.client_auth.force_authenticate(user=self.user)

        adminstudentapplication_url = reverse('adminstudentapplication-detail',
                                              kwargs={'pk': self.application_admin.pk})
        response = self.client_auth.put(adminstudentapplication_url, data={'selected': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
