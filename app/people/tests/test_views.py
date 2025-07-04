import pytest

from django.urls import reverse

from school.tests.conftest import *  # noqa


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
