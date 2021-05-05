from django.contrib.auth.models import User

import factory


class AndyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = "awarhola@pop.art"
    first_name = "Andrew"
    last_name = "Warhola"
    username = "awarhol"


class SuperAndyFactory(AndyFactory):
    is_superuser = True
    is_active = True
