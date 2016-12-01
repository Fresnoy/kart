from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36


def make_filepath(instance, filename):
    """
    Generate a unique filename for any upload (fix problems with
    accents and such).
    """
    new_filename = "{0}.{1}".format(User.objects.make_random_password(10),
                                    filename.split('.')[-1])

    return "{0}/{1}/{2}".format(
        instance.__class__._meta.app_label,
        instance.__class__.__name__.lower(),
        new_filename
    )


def send_activation_email(user, password):
    # Create activation token URL
    uidb36 = int_to_base36(user.id)
    token = default_token_generator.make_token(user)
    url = reverse('user-activate', kwargs={
        'uidb36': uidb36,
        'token': token,
    })
    # Send email
    message = "<html>\
                  <head></head>\
                  <body>\
                    <p>Bonjour<br>\
                       How are you?<br>\
                       Here is the <a href='{0}'>activation link</a> you wanted.\
                       Password: {1}\
                    </p>\
                  </body>\
                </html>".format(url, password)

    mail_sent = send_mail('Le Fresnoy - Email Activation',
                          message,
                          'pedagogie@lefresnoy.net',
                          [user.email],
                          fail_silently=False)
    return mail_sent
