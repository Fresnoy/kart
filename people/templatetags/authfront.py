from django import template

from rest_framework_jwt.settings import api_settings

from ..models import User

from school.models import StudentApplicationSetup

register = template.Library()


@register.simple_tag
def authfront_reset_password_link(token, email):
    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
    url = ""
    print(register)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    if user is not None:
        custom_infos = user

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(custom_infos)
        front_token = jwt_encode_handler(payload)
        route = "candidature.account.login"

        # reverse('password-reset')
        url = "{0}/{1}/{2}".format(setup.reset_password_url, front_token, route)

    return url
