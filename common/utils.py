from django.contrib.auth.models import User

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
