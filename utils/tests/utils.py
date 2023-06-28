import pytest

from django.core.management import call_command
from django.db.models.constants import LOOKUP_SEP
from django.test import Client
from django.urls import reverse
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User


def first(items):
    return items[0]


def obtain_jwt_token(user):
    c = Client()
    url = reverse('rest_login')

    response = c.post(url, {'username': user.username, 'password': 'p4ssw0rd'})
    assert response.status_code == 200
    assert 'access' in response.json()

    return response.json()


def validate_jwt_token(token, user):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    infos = jwt_decode_handler(token)
    return infos and 'user_id' in infos and User.objects.filter(pk=infos['user_id']).exists()


def parametrize_user_roles(metafunc):
    """
    Dynamic handling for parametrization.
    Allow class driven behavior using orverloading, whereas
    @pytest.mark.parametrize only act as collect time.
    """
    if (
        hasattr(metafunc.cls, '_user_roles')
        and "user_role" in metafunc.fixturenames
        and hasattr(metafunc.cls, '_auth_methods')
        and "auth_method" in metafunc.fixturenames
    ):
        if None in metafunc.cls._user_roles:
            # avoid parametrizing auth method when user is anonymous
            parametrization = [(None, None)] + list(zip(
                [r for r in metafunc.cls._user_roles if r is not None],
                metafunc.cls._auth_methods,
            ))
        else:
            parametrization = zip(metafunc.cls._user_roles, metafunc.cls._auth_methods)

        metafunc.parametrize(['user_role', 'auth_method'], parametrization)
    elif hasattr(metafunc.cls, '_user_roles') and "user_role" in metafunc.fixturenames:
        metafunc.parametrize('user_role', metafunc.cls._user_roles)
    elif hasattr(metafunc.cls, '_auth_methods') and "auth_method" in metafunc.fixturenames:
        metafunc.parametrize('auth_method', metafunc.cls._auth_methods)


class AbstractHelpTestForAPI:
    """
    Help to test interfaces to Rest API
    """

    fixtures = []

    methods_behavior = {
        method: 200
        for method in ['list', 'get', 'patch', 'put', 'post', 'delete']
    }

    mutate_fields = []
    hyperlinked_fields = {}
    renamed_fields = {}
    built_fields = {}

    _user_roles = [None, 'user']
    _auth_methods = ['forced', 'jwt']

    @property
    def base_url(self):
        return "{}/{}".format(self.url_prefix, self.uri)

    def setup_fixtures(self, request):
        for fixture_name in self.fixtures:
            setattr(self, fixture_name, request.getfixturevalue(fixture_name))

    def thats_all_folk(self, method, response, user_role):
        if method in self.methods_behavior:
            expected = self.methods_behavior[method]
            if not isinstance(expected, int):
                expected = expected[user_role]
            print("{} -- test code : {} / expected code : {}".format(method, response.status_code, expected))
            assert response.status_code == expected
            return response.status_code not in [200, 204]
        else:
            return True

    def target(self):
        return getattr(self, self.fixtures[0])

    def requestor(self, role):
        if role == 'user':
            return self.user
        if role == 'artist':
            return self.artist.user

    def prepare_request(self, client, user_role, auth_method, data=None, json=True):
        kwargs = {}

        if user_role in ['artist', 'user']:
            if auth_method == 'forced':
                client.force_login(self.requestor(user_role))
            elif auth_method == 'jwt':
                jwt = obtain_jwt_token(self.requestor(user_role))
                kwargs['HTTP_AUTHORIZATION'] = 'JWT {}'.format(jwt['access'])

        if json:
            kwargs['content_type'] = 'application/json'

        if data is not None:
            kwargs['data'] = data

        return kwargs

    def get_data(self, field):
        if field in self.hyperlinked_fields:
            return self.reverse_hyperlink(field)
        elif field in self.renamed_fields:
            return getattr(self.target(), self.renamed_fields[field])
        elif field in self.built_fields:
            return self.built_fields[field](self.target())
        else:
            return getattr(self.target(), field)

    def check_expected_fields(self, obj):
        for field in self.expected_fields:
            if LOOKUP_SEP in field:
                next_obj = obj
                for lookup_field in field.split(LOOKUP_SEP):
                    assert lookup_field in next_obj
                    next_obj = next_obj.get(lookup_field)
            else:
                assert field in obj

    def test_list(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)

        kwargs = self.prepare_request(client, user_role, auth_method)
        response = client.get(self.base_url, **kwargs)

        if self.thats_all_folk('list', response, user_role):
            return

        answer = response.json()

        self.validate_list(answer)

    def test_get(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)

        kwargs = self.prepare_request(client, user_role, auth_method)
        response = client.get('{}/{}'.format(self.base_url, self.target_uri_suffix()), **kwargs)

        if self.thats_all_folk('get', response, user_role):
            return

        answer = response.json()

        self.check_expected_fields(answer)

    def test_post(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)

        fields = getattr(self, 'post_fields', getattr(self, 'put_fields', self.mutate_fields))
        data = {f: self.get_data(f) for f in fields}
        kwargs = self.prepare_request(client, user_role, auth_method, data)
        response = client.post(self.base_url, **kwargs)

        if self.thats_all_folk('post', response, user_role):
            return

    def test_put(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)

        fields = getattr(self, 'put_fields', self.mutate_fields)
        data = {f: self.get_data(f) for f in fields}
        kwargs = self.prepare_request(client, user_role, auth_method, data)
        response = client.put('{}/{}'.format(self.base_url, self.target_uri_suffix()), **kwargs)

        if self.thats_all_folk('put', response, user_role):
            return

    def test_patch(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)

        data = {f: self.get_data(f) for f in self.mutate_fields}
        kwargs = self.prepare_request(client, user_role, auth_method, data)
        response = client.patch('{}/{}'.format(self.base_url, self.target_uri_suffix()), **kwargs)

        if self.thats_all_folk('patch', response, user_role):
            return

    def test_delete(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)

        kwargs = self.prepare_request(client, user_role, auth_method)
        response = client.delete('{}/{}'.format(self.base_url, self.target_uri_suffix()), **kwargs)

        if self.thats_all_folk('delete', response, user_role):
            return


class HelpTestForModelViewSet(AbstractHelpTestForAPI):
    """
    Help to test interfaces to ModelViewSet (DRF)
    """
    url_prefix = "/v2"

    methods_behavior = {
        'list': {None: 401, 'user': 200},
        'get': {None: 401, 'user': 200},
        'patch': {None: 401, 'user': 403},
        'put': {None: 401, 'user': 403},
        'post': {None: 401, 'user': 403},
        'delete': {None: 401, 'user': 403},
    }

    @property
    def uri(self):
        return self.viewset_name

    def target_uri_suffix(self):
        return self.target().pk

    def validate_list(self, answer):
        assert len(answer) == self.expected_list_size

        for ressource in answer:
            self.check_expected_fields(ressource)

    def reverse_hyperlink(self, field):
        return reverse(
            '{}-detail'.format(self.hyperlinked_fields[field]),
            kwargs={'pk': getattr(self.target(), field).pk},
        )


class IsAuthenticatedOrReadOnlyModelViewSetMixin:
    methods_behavior = {
        'list': 200,
        'get': 200,
        'patch': {None: 401, 'user': 200},
        'put': {None: 401, 'user': 200},
        'post': {None: 401, 'user': 201},
        'delete': {None: 401, 'user': 204},
    }


class IsArtistOrReadOnlyModelViewSetMixin:
    _user_roles = [None, 'user', 'artist']

    methods_behavior = {
        'list': 200,
        'get': 200,
        'patch': {None: 401, 'user': 403, 'artist': 200},
        'put': {None: 401, 'user': 403, 'artist': 200},
        'post': {None: 401, 'user': 403, 'artist': 201},
        'delete': {None: 401, 'user': 403, 'artist': 204},
    }


class ReadOnlyModelViewSetMixin:
    methods_behavior = {
        'list': 200,
        'get': 200,
        'patch': {None: 401, 'user': 403},
        'put': {None: 401, 'user': 403},
        'post': {None: 401, 'user': 403},
        'delete': {None: 401, 'user': 403},
    }


class IgnoreModelViewSetMixin:
    methods_behavior = {}

    @pytest.mark.skip()
    def test_list(self):
        pass

    @pytest.mark.skip()
    def test_get(self):
        pass

    @pytest.mark.skip()
    def test_patch(self):
        pass

    @pytest.mark.skip()
    def test_put(self):
        pass

    @pytest.mark.skip()
    def test_post(self):
        pass

    @pytest.mark.skip()
    def test_delete(self):
        pass


class HelpTestForModelRessource(AbstractHelpTestForAPI):
    """
    Help to test interfaces to ModelResource (tastypie)
    """
    url_prefix = "/v1"

    @property
    def uri(self):
        return self.resource._meta.resource_name

    def target_uri_suffix(self):
        return getattr(self.target(), self.resource._meta.detail_uri_name)

    def validate_list(self, answer):
        assert "meta" in answer
        assert "objects" in answer
        assert len(answer["objects"]) == self.expected_list_size

        for ressource in answer["objects"]:
            self.check_expected_fields(ressource)

    def reverse_hyperlink(self, field):
        resource_name = self.hyperlinked_fields[field]
        key = 'username' if resource_name == 'people/user' else 'pk'
        kwargs = {
            'api_name': 'v1',
            'resource_name': resource_name,
            key: getattr(getattr(self.target(), field), key)
        }
        return reverse('api_dispatch_detail', kwargs=kwargs)


class HelpTestForReadOnlyModelRessource(HelpTestForModelRessource):
    _user_roles = [None]

    methods_behavior = {
        'list': 200,
        'get': 200,
        'patch': 401,
        'put': 401,
        'post': 401,
        'delete': 401,
    }


class FilterModelRessourceMixin:

    search_field = None

    def test_search(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)

        data = {self.search_field: getattr(self.target(), self.search_field)}
        kwargs = self.prepare_request(client, user_role, auth_method, data)
        response = client.get(self.base_url, **kwargs)

        if self.thats_all_folk('list', response, user_role):
            return

        answer = response.json()

        assert "meta" in answer
        assert "objects" in answer
        assert len(answer["objects"]) == 1

        self.check_expected_fields(answer["objects"][0])


class HaystackSearchModelRessourceMixin:

    search_suffix = '/search'
    search_param = 'q'
    search_field = None

    def test_haystack_search(self, client, user_role, auth_method, request):
        self.setup_fixtures(request)
        call_command('rebuild_index', verbosity=0, interactive=False)

        data = {self.search_param: getattr(self.target(), self.search_field)}
        kwargs = self.prepare_request(client, user_role, auth_method, data, json=False)
        response = client.get(self.base_url + self.search_suffix, **kwargs)
        if self.thats_all_folk('list', response, user_role):
            return

        answer = response.json()

        assert "objects" in answer
        assert len(answer["objects"]) == 1

        kwargs['data']['page'] = '-1'
        response = client.get(self.base_url + self.search_suffix, **kwargs)
        assert response.status_code == 404

        kwargs['data']['page'] = 'none'
        response = client.get(self.base_url + self.search_suffix, **kwargs)
        assert response.status_code == 400
