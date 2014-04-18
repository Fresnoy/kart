from django.db import models

from production.models import Installation, Film, Performance

class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Award(models.Model):
    """
    Awards given to artworks & such.
    """
    pass


class Event(models.Model):
    TYPE_CHOICES = (
        ('PROJ', 'Projection'),
        ('EXHIB', 'Exhibition'),
        ('VARN', 'Varnishing'),
        ('PARTY', 'Party'),
        ('WORKSHOP', 'Workshop'),
        ('EVENING', 'Evening')
    )
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    
    website = models.URLField(blank=True, null=True)
    place = models.ForeignKey(Place)

    picture = models.ImageField(upload_to='events/')

    # artwork types
    installations = models.ManyToManyField(Installation, blank=True, related_name='events')
    films = models.ManyToManyField(Film, blank=True, related_name='events')
    performances = models.ManyToManyField(Performance, blank=True, related_name='events')

    subevents = models.ManyToManyField('self', blank=True)
    