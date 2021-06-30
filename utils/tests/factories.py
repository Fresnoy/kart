import factory

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class Password(factory.declarations.LazyFunction):
    """
    Inspired from FactoryBoy last upstream
    """

    def __init__(self, password, *args, **kwargs):
        super().__init__(make_password, *args, **kwargs)
        self.value = password

    def evaluate(self, instance, step, extra):
        return self.function(self.value)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    password = Password('p4ssw0rd')


class AdminFactory(UserFactory):
    is_superuser = True
    is_active = True
    is_staff = True
