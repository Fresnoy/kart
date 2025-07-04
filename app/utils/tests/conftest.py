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
    # FIXME: amha ça mériterais une migration
    perms = [
        "add_corsmodel",
        "add_filmgenre",
        "add_gallery",
        "add_medium",
        "add_promotion",  # FIXME: a priori pas nécessaire
        "add_stafftask",
        "add_student",
        "add_studentapplication",
        "add_studentapplicationsetup",
        "add_userobjectpermission",
        "add_website",
        "change_corsmodel",
        "change_filmgenre",
        "change_gallery",
        "change_medium",
        "change_promotion",
        "change_stafftask",
        "change_student",
        "change_studentapplication",
        "change_studentapplicationsetup",
        "change_userobjectpermission",
        "change_website",
        "delete_corsmodel",
        "delete_filmgenre",
        "delete_gallery",
        "delete_medium",
        "delete_promotion",
        "delete_student",
        "delete_studentapplication",
        "delete_studentapplicationsetup",
        "delete_userobjectpermission",
        "delete_website",
    ]

    group = Group.objects.create(name='School Application')
    group.permissions.set(Permission.objects.filter(codename__in=perms))
    return group
