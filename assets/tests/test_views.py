import json
import pytest

from django.urls import reverse
from pytest_django.asserts import assertContains

from utils.tests.utils import obtain_jwt_token


@pytest.mark.django_db
class TestVimeoUploadToken:
    @pytest.mark.parametrize(
        'user_role, expected', [
            (None, 200),
            ('user', 200),
            ('old_user', 200),
        ]
    )
    def test_vimeo_get_upload_token(self, client, user_role, expected, user, student_application_setup):
        url = reverse('vimeo-upload-token')

        if user_role:
            jwt = obtain_jwt_token(user)
            if user_role == 'old_user':
                user.delete()
            response = client.get(url, HTTP_AUTHORIZATION='JWT {}'.format(jwt['token']))
        else:
            response = client.get(url)

        assert response.status_code == expected

        if user_role == 'user':
            # FIXME: je ne m'attendais pas à recevoir du json avec un Content-Type header is "text/html.
            token = json.loads(response.content.decode())
            assert token
            for key in ['name', 'url', 'token']:
                assert key in token
        else:
            assertContains(response, "Not Authenticated")
