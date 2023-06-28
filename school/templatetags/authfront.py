from django import template

from rest_framework_simplejwt.tokens import RefreshToken

from people.models import User

from school.models import StudentApplicationSetup

register = template.Library()


@register.simple_tag
def authfront_reset_password_link(token, email):
    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
    url = ""

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    if user is not None:

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        route = "candidature.account.login"

        # reverse('password-reset')
        url = "{0}/{1}/{2}".format(setup.reset_password_url, access_token, route)

    return url
