from django.db import models

from uuidfield import UUIDField

class BTBeacon(models.Model):
    label = models.CharField(max_length=255)
    uuid = UUIDField(unique=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.label, self.uuid)

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
    
