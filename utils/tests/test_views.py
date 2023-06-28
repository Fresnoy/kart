import pytest

from django.urls import reverse

from utils.tests.utils import obtain_jwt_token, validate_jwt_token


@pytest.mark.django_db
class TestJWTToken:
    @pytest.mark.parametrize(
        'user_role, expected', [
            (None, 400),
            ('user', 201),
            ('admin', 201),
            ('inactive_user', 400),
            ('joker', 400),
        ]
    )
    def test_raw_obtain_jwt_token(self, client, user_role, expected, user, admin, joker, inactive_user):
        url = reverse('obtain-jwt-token')
        data = {}
        if user_role:
            requestor = locals().get(user_role)
            data['username'] = requestor.username
            data['password'] = 'p4ssw0rd'

        response = client.post(url, data=data)

        assert response.status_code == expected
        if expected == 200:
            json_response = response.json()
            assert 'access' in json_response
            assert validate_jwt_token(json_response['access'], user)

    def test_obtain_jwt_token(self, client, user):
        jwt = obtain_jwt_token(user)['access']
        assert validate_jwt_token(jwt, user)
