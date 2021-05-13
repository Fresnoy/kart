import pytest

from django.contrib.auth.models import Group, Permission

from . import factories


@pytest.fixture
def db_ready(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock() as db:
        return db


@pytest.fixture
def user(db_ready):
    return factories.UserFactory()


@pytest.fixture
def inactive_user(db_ready):
    return factories.UserFactory(is_active=False)


@pytest.fixture
def admin(db_ready):
    return factories.AdminFactory()


@pytest.fixture
def joker(db_ready):
    # return a user-like object nonexistant in db
    return factories.UserFactory.stub()


@pytest.fixture
def school_application_group(db_ready):
    # FIXME: c'est ce que je comprends de la fixture groups.json
    # FIXME: amha ça mériterais une migration
    perms = [
        'view_staff',
        'delete_staff',
        'add_itinerary',
        'change_itinerary',
        'delete_itinerary',
        'view_itinerary',
        'view_organizationtask',
        'delete_organizationtask',
        'add_production',
        'add_taggeditem',
        'change_taggeditem',
    ]

    group = Group.objects.create(name='School Application')
    group.permissions.set(Permission.objects.filter(codename__in=perms))
    return group
