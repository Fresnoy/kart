from django.db import models

from diffusion.models import Place

from model_utils.managers import InheritanceManager

from people.models import Artist, Staff, Organization
from assets.models import Gallery

class Task(models.Model):
    class Meta:
        abstract = True
        
    label = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.label

class StaffTask(Task):
    pass

class OrganizationTask(Task):
    pass

class ProductionStaffTask(models.Model):
    staff = models.ForeignKey(Staff)
    production = models.ForeignKey('Production')
    task = models.ForeignKey(StaffTask)
    
class ProductionOrganizationTask(models.Model):
    organization = models.ForeignKey(Organization)
    production = models.ForeignKey('Production')
    task = models.ForeignKey(StaffTask)
   
class Production(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    picture = models.ImageField(upload_to='production/')
    website = models.URLField(blank=True, null=True)

    collaborators = models.ManyToManyField(Staff, through=ProductionStaffTask, blank=True, related_name="%(class)s")
    partners = models.ManyToManyField(Organization, through=ProductionOrganizationTask, blank=True, related_name="%(class)s")

    description_short_fr = models.TextField(blank=True, null=True)
    description_short_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.title


class SubclassesManager(InheritanceManager):
    """
    http://stackoverflow.com/a/20998123
    """
    def get_queryset(self):
        return super(SubclassesManager, self).get_queryset().select_subclasses()
    
class Artwork(Production):
    production_date = models.DateField()
    
    credits_fr = models.TextField(blank=True, null=True)
    credits_en = models.TextField(blank=True, null=True)

    thanks_fr = models.TextField(blank=True, null=True)
    thanks_en = models.TextField(blank=True, null=True)

    copyright_fr = models.TextField(blank=True, null=True)
    copyright_en = models.TextField(blank=True, null=True)
    
    process_galleries = models.ManyToManyField(Gallery, blank=True, related_name='artworks_process')
    mediation_galleries = models.ManyToManyField(Gallery, blank=True, related_name='artworks_mediation')
    in_situ_galleries = models.ManyToManyField(Gallery, blank=True, related_name='artworks_insitu')

    authors = models.ManyToManyField(Artist, related_name="%(class)s")

    objects = SubclassesManager()
    
    
class Film(Artwork):
    pass

class Installation(Artwork):
    technical_description = models.TextField(blank=True)

class Performance(Artwork):
    pass

class Event(Production):
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
    
    place = models.ForeignKey(Place)

    # artwork types
    installations = models.ManyToManyField(Installation, blank=True, related_name='events')
    films = models.ManyToManyField(Film, blank=True, related_name='events')
    performances = models.ManyToManyField(Performance, blank=True, related_name='events')

    subevents = models.ManyToManyField('self', blank=True)

class Exhibition(Event):
    pass # TODO?

class Itinerary(models.Model):
    class Meta:
        verbose_name_plural = 'itineraries'
    
    label = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey(Event, limit_choices_to={'type': 'EXHIB'}, related_name='itineraries')
    artworks = models.ManyToManyField(Artwork, through='ItineraryArtwork')

    def __unicode__(self):
        return self.label

class ItineraryArtwork(models.Model):
    class Meta:
        ordering = ('order',)
        unique_together = (('itinerary', 'artwork'), ('itinerary', 'order'))
        
    itinerary = models.ForeignKey(Itinerary)
    artwork = models.ForeignKey(Artwork)
    order = models.PositiveIntegerField()

