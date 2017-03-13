# -*- coding: utf-8 -*-
from django.db import models

from polymorphic.models import PolymorphicModel
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
    production = models.ForeignKey('Production', related_name="staff_tasks")
    task = models.ForeignKey(StaffTask)


class ProductionOrganizationTask(models.Model):
    organization = models.ForeignKey(Organization)
    production = models.ForeignKey('Production', related_name="organization_tasks")
    task = models.ForeignKey(OrganizationTask)


class Production(PolymorphicModel):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=255)
    former_title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)

    updated_on = models.DateTimeField(auto_now=True)

    picture = models.ImageField(upload_to=make_filepath)
    websites = models.ManyToManyField(Website, blank=True)

    collaborators = models.ManyToManyField(Staff, through=ProductionStaffTask, blank=True, related_name="%(class)s")
    partners = models.ManyToManyField(Organization,
                                      through=ProductionOrganizationTask, blank=True,
                                      related_name="%(class)s")

    description_short_fr = models.TextField(blank=True, null=True)
    description_short_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "{0} ({1})".format(self.title, self.id)


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
        ('1.33', "1.33 (4/3)"),
        ('1.37', "1.37"),
        ('1.66', "1.66"),
        ('1.77', "1.77 (16/9)"),
        ('1.85', "1.85 (Flat)"),
        ('1.90', "1.90 (Full Container)"),
        ('2.39', "2.39 (Scope)"),

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
    pass  # TODO?


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
