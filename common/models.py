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

    def __unicode__(self):
        return self.title_fr
