from django.test import Client
from django.urls import reverse
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User


def first(items):
    return items[0]


def obtain_jwt_token(user):
    c = Client()
    url = reverse('obtain-jwt-token')

    response = c.post(url, {'username': user.username, 'password': 'p4ssw0rd'})
    assert response.status_code == 200
    assert 'token' in response.json()

    return response.json()


def validate_jwt_token(token, user):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    infos = jwt_decode_handler(token)
    return infos and 'user_id' in infos and User.objects.filter(pk=infos['user_id']).exists()
