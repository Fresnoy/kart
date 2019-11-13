import os
import datetime
from kart import settings


def make_filepath(instance, filename, prefix_folder=None):
    """Generate a unique path and filename for any upload (fix problmes with accents and such)"""

    # Root directory for media
    _r = settings.MEDIA_ROOT
    # Context directory
    context_dir = os.path.join(instance.__class__._meta.app_label,
                               instance.__class__.__name__.lower())
    # Date directory
    _t = datetime.datetime.today()
    date_dir = "{}/{}".format(_t.strftime('%Y'), _t.strftime('%m'))

    # TODO : explore instance to look for user or production reference
    # _uss = instance._meta.get_field('user')

    dest_folder = os.path.join(_r, context_dir, date_dir, filename)
    return dest_folder
