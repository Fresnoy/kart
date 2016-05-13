# -*- coding: utf-8 -*-
from django.db import models

from model_utils.managers import InheritanceManager
from sortedm2m.fields import SortedManyToManyField

from assets.models import Gallery
from common.models import Website, BTBeacon
from common.utils import make_filepath
from diffusion.models import Place
from people.models import Artist, Staff, Organization


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
    task = models.ForeignKey(OrganizationTask)

class Production(models.Model):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=255)
    former_title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)

    updated_on = models.DateTimeField(auto_now=True)

    picture = models.ImageField(upload_to=make_filepath)
    websites = models.ManyToManyField(Website, blank=True)

    collaborators = models.ManyToManyField(Staff, through=ProductionStaffTask, blank=True, related_name="%(class)s")
    partners = models.ManyToManyField(Organization, through=ProductionOrganizationTask, blank=True, related_name="%(class)s")

    description_short_fr = models.TextField(blank=True, null=True)
    description_short_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)

    def __unicode__(self):
        # return "Production %s" % self.id
        return "%s - %s" % (self.title,self.id)


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

    process_galleries = SortedManyToManyField(Gallery, blank=True, related_name='artworks_process')
    mediation_galleries = SortedManyToManyField(Gallery, blank=True, related_name='artworks_mediation')
    in_situ_galleries = SortedManyToManyField(Gallery, blank=True, related_name='artworks_insitu')
    press_galleries = SortedManyToManyField(Gallery, blank=True, related_name='artworks_press')
    teaser_galleries = SortedManyToManyField(Gallery, blank=True, related_name='artworks_teaser')

    authors = models.ManyToManyField(Artist, related_name="%(class)ss")

    beacons = models.ManyToManyField(BTBeacon, related_name="%(class)ss", blank=True)

    objects = SubclassesManager()

class FilmGenre(models.Model):
    label = models.CharField(max_length=100)

    def __unicode__(self):
        return self.label

class Film(Artwork):
    SHOOTING_FORMAT_CHOICES = (
        ('SUP8', 'Super 8'),
        ('SUP16', 'Super 16'),
        ('SUP35', 'Super 35'),
        ('35MM', "35 MM"),
        ('70MM', "70 MM"),
        ('DV', "DV"),
        ('DVCAM', "DV-CAM"),
        ('HD', "HD"),
        ('HDCAM', "HD-CAM"),
        ('HDCINE', "HD CINEMASCOPE"),
        ('CREANUM', "CREATION NUMERIQUE"),
        ('BETASP', "BETA SP"),
        ('BETANUM', "BETA NUM."),
        ('DIGICAM', "APPAREIL PHOTO"),
        ('MOBILE', "MOBILE"),
        ('HI8', "HI8"),
        ('AVCHD', "AVCHD"),
        ('XDCAMEX', "XDcamEX"),
        ('3DREL', "RELIEF 3D"),
        ('2K', "2K"),
        ('4K', "4K")
    )

    ASPECT_RATIO_CHOICES = (
        ('1.33', "1.33"),
        ('1.37', "1.37"),
        ('1.66', "1.66"),
        ('1.77', "1.77"),
        ('1.85', "1.85"),
        ('1.89', "1.89"),
        ('2.35', "2.35"),
        ('4/3', "4/3"),
        ('16/9', "16/9")
    )

    PROCESS_CHOICES = (
        ('COLOR', "Couleur"),
        ('BW', "Noir & Blanc"),
        ('COLORBW', "NB & Couleur"),
        ('SEPIA', "Sépia")
    )
    duration = models.DurationField(blank=True, null=True, help_text="Sous la forme HH:MM:SS")
    shooting_format = models.CharField(choices=SHOOTING_FORMAT_CHOICES, max_length=10, blank=True)
    aspect_ratio = models.CharField(choices=ASPECT_RATIO_CHOICES, max_length=10, blank=True)
    process = models.CharField(choices=PROCESS_CHOICES, max_length=10, blank=True)
    genres = models.ManyToManyField(FilmGenre)

class InstallationGenre(models.Model):
    label = models.CharField(max_length=100)

    def __unicode__(self):
        return self.label

class Installation(Artwork):
    technical_description = models.TextField(blank=True)
    genres = models.ManyToManyField(InstallationGenre)

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

    updated_on = models.DateTimeField(auto_now=True)

    label_fr = models.CharField(max_length=255)
    label_en = models.CharField(max_length=255)
    description_fr = models.TextField()
    description_en = models.TextField()
    event = models.ForeignKey(Event, limit_choices_to={'type': 'EXHIB'}, related_name='itineraries')
    artworks = models.ManyToManyField(Artwork, through='ItineraryArtwork')
    gallery = models.ManyToManyField(Gallery, blank=True, related_name='itineraries')

    def __unicode__(self):
        return self.label_fr

class ItineraryArtwork(models.Model):
    class Meta:
        ordering = ('order',)
        unique_together = (('itinerary', 'artwork'), ('itinerary', 'order'))

    itinerary = models.ForeignKey(Itinerary)
    artwork = models.ForeignKey(Artwork)
    order = models.PositiveIntegerField()

from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=Performance)
@receiver(post_delete, sender=Film)
@receiver(post_delete, sender=Installation)
def delete_parent(sender, instance, using, **kwargs):
    print("delete parent!")
