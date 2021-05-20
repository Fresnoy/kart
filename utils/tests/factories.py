from django.contrib.auth.models import User

import factory


factory.Faker._DEFAULT_LOCALE = 'fr_FR'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')


class AdminFactory(UserFactory):
    is_superuser = True
    is_active = True
