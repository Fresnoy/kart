from uuidfield import UUIDField

from django.db import models


class BTBeacon(models.Model):
    label = models.CharField(max_length=255)
    uuid = UUIDField(unique=True)
    rssi_in = models.IntegerField()
    rssi_out = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    def __unicode__(self):
        return "{0} ({1})".format(self.label, self.uuid)


class Website(models.Model):
    LANGUAGES = (
        ('FR', 'French'),
        ('EN', 'English')
    )
    title_fr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    language = models.CharField(choices=LANGUAGES, max_length=2)
    url = models.URLField()

    def __unicode__(self):
        return self.title_fr
