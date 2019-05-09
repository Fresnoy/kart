from django.db import models


class Website(models.Model):
    """ Dedicated model for websites.

    """
    LANGUAGES = (
        ('FR','Français'),
        ('EN','English'),

    )
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    language = models.CharField(choices=LANGUAGES, max_length=2)
    url = models.URLField()

    def __str__(self):
        """Return the litterate form of a website.
        Example : Le site du Fresn(...) - http://www.lefresnoy.net
        """
        return "{}(...) - {}".format(self.title_fr[10],url[40])
