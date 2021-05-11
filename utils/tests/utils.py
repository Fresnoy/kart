from django.test import Client
from django.urls import reverse


def first(items):
    return items[0]


def obtain_jwt_token(user):
    c = Client()
    url = reverse('obtain-jwt-token')

    response = c.post(url, {'username': user.username, 'password': 'p4ssw0rd'})
    assert response.status_code == 200
    assert 'token' in response.json()

    return response.json()
