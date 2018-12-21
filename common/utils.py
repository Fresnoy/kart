import os
import datetime
from django.contrib.auth.models import User
from kart import settings


def make_filepath(instance, filename, prefix_folder=None):
    """
    Generate a unique filename for any upload (fix problems with
    accents and such).
    """

    carry_on = True
    default_folder = datetime.datetime.today().strftime('%Y')
    while carry_on:
        new_filename = "{0}.{1}".format(User.objects.make_random_password(10),
                                        filename.split('.')[-1])
        path = "{0}/{1}/{2}/{3}".format(
            instance.__class__._meta.app_label,
            instance.__class__.__name__.lower(),
            # prefix or year ( = not empty) to prevent 'app/class//file.fmt'
            prefix_folder or default_folder,
            new_filename
        )
        carry_on = os.path.isfile(os.path.join(settings.MEDIA_ROOT, path))

    return path
