from django.db import models

from common.utils import make_filepath

class Gallery(models.Model):
    """
    A named collection of Media
    """
    label = models.CharField(max_length=255)
    description = models.TextField()

    updated_on = models.DateTimeField(auto_now=True)    

    def __unicode__(self):
        return u"%s - %s" % (self.label, self.description)

    class Meta:
        verbose_name_plural = "galleries"


class Medium(models.Model):
    """
    Anything that looks like a file.
    """
    updated_on = models.DateTimeField(auto_now=True)
    
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to=make_filepath, null=True, blank=True)
    medium_url = models.URLField(null=True, blank=True)

    gallery = models.ForeignKey(Gallery, related_name='media')

    def __unicode__(self):
        return u"%s - %s" % (self.label, self.description)

    class Meta:
        verbose_name_plural = "media"
        

