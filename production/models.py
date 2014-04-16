from django.db import models

from people.models import Artist
from diffusion.models import Place
from assets.models import Gallery

class Production(models.Model):
    class Meta:
        abstract = True
        
    production_date = models.DateField()
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)    

    description_short_fr = models.TextField(blank=True, null=True)
    description_short_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    
    galleries = models.ManyToManyField(Gallery, blank=True)

    authors = models.ManyToManyField(Artist, related_name="%(class)s")

    def __unicode__(self):
        return u"%s" % self.title
    
    
class Artwork(Production):
    class Meta:
        abstract = True

    credits_fr = models.TextField(blank=True, null=True)
    credits_en = models.TextField(blank=True, null=True)

    
class Film(Artwork):
    pass

class Installation(Artwork):
    technical_description = models.TextField(blank=True)

class Event(Production):
    TYPE_CHOICES = (
        ('EVENT', 'Event'),
        ('SHOW', 'Show'),
        ('PERF', 'Performance'),
        ('THEATRE', 'Theatre'),
        ('PROJ', 'Projection'),
        ('EXHIB', 'Exhibition'),
        ('VARN', 'Varnishing'),
        ('PARTY', 'Party'),
        ('WORKSHOP', 'Workshop'),
        ('EVENING', 'Evening')
    )
    
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    website = models.URLField(blank=True, null=True)
    place = models.ForeignKey(Place)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    subevents = models.ManyToManyField('self')


class Task(models.Model):
    pass