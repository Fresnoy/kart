import re
import pytest

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import int_to_base36
from pytest_django.asserts import assertContains

from utils.tests.utils import validate_jwt_token
from school.tests.conftest import *  # noqa

from ..models import User


@pytest.mark.django_db
class TestUserActivation:
    def munge(self, string):
        old_c = string[0]
        new_c = 'I' if old_c.isnumeric() else '9'
        return new_c + string[1:]

    @pytest.mark.parametrize(
        'use_case, expected_code, expected_email, expected_text', [
            ('bad_uid', 200, 0, "Erreur d'activation"),
            ('bad_token', 200, 0, "a déjà été validé"),  # FIXME: actually it seems unexpected
            ('deleted_user', 200, 0, "Erreur d'activation"),
            ('secret_changed', 200, 0, "a déjà été validé"),
            ('active_user', 302, 1, None),  # FIXME: actually it seems unexpected
        ]
    )
    def test_activation_attempts(
            self, use_case, expected_code, expected_email,
            expected_text, client, user, mailoutbox, student_application_setup):

        uidb36 = int_to_base36(user.id)
        token = default_token_generator.make_token(user)

        if use_case == 'bad_uid':
            uidb36 = self.munge(uidb36)
        elif use_case == 'bad_token':
            token = self.munge(token)
        elif use_case == 'deleted_user':
            user.delete()
        elif use_case == 'secret_changed':
            user.set_password('n3w_p4ssw0rd')
            user.save()
        elif use_case == 'active_user':
            # it is already the case
            pass

        url = reverse('user-activate', kwargs={
            'uidb36': uidb36,
            'token': token,
        })
        response = client.get(url)
        assert response.status_code == expected_code
        assert len(mailoutbox) == expected_email
        if expected_text:
            assertContains(response, expected_text)

    def test_register_activate_for_user(self, client, joker, mailoutbox, student_application_setup):
        """
        Test registration and activation using the normal way.
        """
        # let's register new user
        url = reverse('user-register')
        response = client.post(url, data=joker.__dict__)

        assert response.status_code == 202

        # user has been created
        u = User.objects.get(email=joker.email, is_active=False)

        # without perms
        assert not u.has_perm('change_user')
        assert not u.has_perm('change_user', u)
        assert not u.has_perm('change_fresnoyprofile')
        assert not u.has_perm('change_fresnoyprofile', u.profile)

        # within group
        u.groups.filter(name='School Application').exists()

        # a mail has been sent
        assert len(mailoutbox) == 1
        assert joker.email in mailoutbox[0].to

        # we get register url from email
        match = re.search(r'[^\s]+/account/activate/[^\s]+', mailoutbox[0].body)
        assert match
        url = match.group(0)

        # let's activate it
        response = client.get(url)
        assert response.status_code == 302

        # user has been activated
        u = User.objects.get(email=joker.email, is_active=True)

        # perms has been activated
        assert not u.has_perm('change_user')
        assert u.has_perm('change_user', u)
        assert not u.has_perm('change_fresnoyprofile')
        assert u.has_perm('change_fresnoyprofile', u.profile)
        u.groups.filter(name='School Application').exists()

        # a new mail has been sent
        # FIXME: we should test authentification_url and recover_password_url from email
        assert len(mailoutbox) == 2
        assert joker.email in mailoutbox[1].to

        # the JWT obtained in web redirection is valid
        match = re.search(r'[^\s]*/([^\s]+)/candidature\.account\.login', response.url)
        assert match
        jwt = match.group(1)
        assert validate_jwt_token(jwt, u)


@pytest.mark.django_db
class TestSendCustomEmails:
    @pytest.mark.parametrize(
        'user_role, method, expected_code, expected_email', [
            (None, 'post', 401, 0),
            ('user', 'post', 401, 0),
            ('admin', 'post', 200, 1),
            ('staff', 'get', 406, 0),
            ('staff', 'post', 200, 1),
            ('staff_bad_request', 'post', 406, 0),
            ('staff_bad_email', 'post', 403, 0),
            ('staff_old', 'post', 401, 0),
        ]
    )
    def test_send_custom_emails(
            self, user_role, method, expected_code, expected_email, faker,
            client, user, admin, mailoutbox, student_application_setup):

        data = {
            'from': user.email,
            'to': user.email,
            'bcc': admin.email,
            'subject': faker.sentence(),
            'message': faker.paragraph(),
        }

        if user_role and user_role.startswith('staff'):
            user.is_staff = True
            user.save()
            client.force_login(user)

            if user_role == 'staff_bad_request':
                data.pop('subject')
            elif user_role == 'staff_bad_email':
                data['from'] = 'nobody_at_nowhere'
            elif user_role == 'staff_old':
                user.is_active = False
                user.save()

        elif user_role:
            client.force_login(locals().get(user_role))

        url = reverse('send-emails')
        response = getattr(client, method)(url, data=data)

        assert response.status_code == expected_code
        assert len(mailoutbox) == expected_email
