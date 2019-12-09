from django.db import models


class Website(models.Model):
    """ Dedicated model for websites.

    """
    LANGUAGES = (
        ('FR', 'Français'),
        ('EN', 'English'),

    )
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    language = models.CharField(choices=LANGUAGES, max_length=2)
    url = models.URLField()

    def __str__(self):
        """Return the litterate form of a website.
        Example : Le site du Fresn(...) - http://www.lefresnoy.net
        """
        title = (self.title_fr[:20] + '(...)' if len(self.title_fr) > 20
                 else self.title_fr)
        return "{} - {:40}".format(title, self.url)


class BTBeacon(models.Model):
    label = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True)
    rssi_in = models.IntegerField()
    rssi_out = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return '{0} ({1})'.format(self.label, self.uuid)
