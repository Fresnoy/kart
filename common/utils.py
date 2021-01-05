import os
import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from kart import settings


def make_filepath(instance, filename, prefix_folder=None):
    """Generate a unique path and filename for any upload (fix problmes with accents and such)"""

    # Date directory
    _t = datetime.datetime.today()
    # slug filename
    default_folder = "{}/{}".format(_t.strftime('%Y'), _t.strftime('%m'))
    # get file name and extension (with '.')
    file_name, file_extension = os.path.splitext(filename)
    # truncate long filename without accent and such
    file_name = slugify(file_name)[:50]
    # making unique file in path
    carry_on = True
    while carry_on:
        new_filename = "{name}_{random}{extension}".format(name=file_name,
                                                           random=User.objects.make_random_password(3),
                                                           extension=file_extension)
        path = "{app}/{model}/{date}/{name}".format(
            app=instance.__class__._meta.app_label,
            model=instance.__class__.__name__.lower(),
            # prefix or date ( = not empty) to prevent 'app/class//file.fmt'
            date=prefix_folder or default_folder,
            name=new_filename
        )
        carry_on = os.path.isfile(os.path.join(settings.MEDIA_ROOT, path))
    return path
