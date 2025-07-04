# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

from polymorphic.models import PolymorphicModel
from sortedm2m.fields import SortedManyToManyField

import pytz

from taggit.managers import TaggableManager

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

    def __str__(self):
        return self.label


class StaffTask(Task):
    pass


class OrganizationTask(Task):
    pass


class ProductionStaffTask(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    production = models.ForeignKey(
        'Production', related_name="staff_tasks", on_delete=models.CASCADE)
    task = models.ForeignKey(StaffTask, on_delete=models.PROTECT)

    def __str__(self):
        return '{0} ({1})'.format(self.task.label, self.production.title)

    class Meta:
        ordering = ['pk']


class ProductionOrganizationTask(models.Model):
    organization = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL)
    production = models.ForeignKey(
        'Production', related_name="organization_tasks", on_delete=models.PROTECT)
    task = models.ForeignKey(OrganizationTask, on_delete=models.PROTECT)

    class Meta:
        ordering = ['pk']


class Production(PolymorphicModel):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=255)
    former_title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)

    updated_on = models.DateTimeField(auto_now=True)

    picture = models.ImageField(upload_to=make_filepath, blank=True)
    websites = models.ManyToManyField(Website, blank=True)

    collaborators = models.ManyToManyField(
        Staff, through=ProductionStaffTask, blank=True, related_name="%(class)s")
    partners = models.ManyToManyField(Organization,
                                      through=ProductionOrganizationTask, blank=True,
                                      related_name="%(class)s")

    description_short_fr = models.TextField(blank=True, null=True)
    description_short_en = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{0}'.format(self.title)


class Artwork(Production):
    production_date = models.DateField()

    credits_fr = models.TextField(blank=True, null=True)
    credits_en = models.TextField(blank=True, null=True)

    thanks_fr = models.TextField(blank=True, null=True)
    thanks_en = models.TextField(blank=True, null=True)

    copyright_fr = models.TextField(blank=True, null=True)
    copyright_en = models.TextField(blank=True, null=True)

    process_galleries = SortedManyToManyField(
        Gallery, blank=True, related_name='artworks_process')
    mediation_galleries = SortedManyToManyField(
        Gallery, blank=True, related_name='artworks_mediation')
    in_situ_galleries = SortedManyToManyField(
        Gallery, blank=True, related_name='artworks_insitu')
    press_galleries = SortedManyToManyField(
        Gallery, blank=True, related_name='artworks_press')
    teaser_galleries = SortedManyToManyField(
        Gallery, blank=True, related_name='artworks_teaser')

    authors = models.ManyToManyField(Artist, related_name="%(class)ss")

    beacons = models.ManyToManyField(
        BTBeacon, related_name="%(class)ss", blank=True)

    keywords = TaggableManager(blank=True,)

    def __str__(self):
        authors = (", ".join([author.__str__() for author in self.authors.all()])
                   if self.authors.count() > 0 else "?")
        return '{0} ({1}), {2} de {3}'.format(self.title, self.production_date.year,
                                              self.polymorphic_ctype.name, authors)


class FilmGenre(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
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
    duration = models.DurationField(
        blank=True, null=True, help_text="Sous la forme HH:MM:SS")
    shooting_format = models.CharField(
        choices=SHOOTING_FORMAT_CHOICES, max_length=10, blank=True)
    aspect_ratio = models.CharField(
        choices=ASPECT_RATIO_CHOICES, max_length=10, blank=True)
    process = models.CharField(
        choices=PROCESS_CHOICES, max_length=10, blank=True)
    genres = models.ManyToManyField(FilmGenre, blank=True)
    shooting_place = models.ManyToManyField(Place, blank=True)


class InstallationGenre(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class Installation(Artwork):
    technical_description = models.TextField(blank=True)
    genres = models.ManyToManyField(InstallationGenre)


class Performance(Artwork):
    pass


def main_event_false_limit():
    return {'pk__in': Event.objects.filter(Q(main_event=False)).values_list('id', flat=True)}


class Event(Production):
    main_event = models.BooleanField(default=False, help_text="Meta Event")

    TYPE_CHOICES = (
        ('FEST', 'Festival'),
        ('COMP', 'Competition'),
        ('PROJ', 'Projection'),
        ('EXHIB', 'Exhibition'),
        ('VARN', 'Varnishing'),
        ('PARTY', 'Party'),
        ('WORKSHOP', 'Workshop'),
        ('EVENING', 'Evening'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField(blank=True, null=True)

    place = models.ForeignKey(Place, null=True, on_delete=models.SET_NULL)

    # artwork types
    installations = models.ManyToManyField(
        Installation, blank=True, related_name='events')
    films = models.ManyToManyField(Film, blank=True, related_name='events')
    performances = models.ManyToManyField(
        Performance, blank=True, related_name='events')
    # subevent can't be main event
    subevents = models.ManyToManyField('Event',
                                       limit_choices_to=main_event_false_limit,
                                       blank=True,
                                       related_name='parent_event')

    def __str__(self):
        if self.parent_event.exists():
            return f"{self.title} ({self.parent_event.first().title})"
        # Events are displayed with their year of edition
        if not self.main_event:
            # Important to convert to Paris Timezone because a datetime 01/01/2015 00:00
            # returns the year 2014 in UTCtime (one hour before 2015) ..
            starting_date = self.starting_date.astimezone(
                pytz.timezone('Europe/Paris'))
            return f"{self.title} - {starting_date.year}"
        # Main events don't have a particular date
        else:
            return f"{self.title} (main event)"


class Exhibition(Event):
    pass  # TODO?


class Itinerary(models.Model):
    '''An itinerary (ordered selection of artworks) throughout an exhibition.
    '''
    class Meta:
        verbose_name_plural = 'itineraries'

    updated_on = models.DateTimeField(auto_now=True)

    label_fr = models.CharField(max_length=255)
    label_en = models.CharField(max_length=255)
    description_fr = models.TextField()
    description_en = models.TextField()
    event = models.ForeignKey(Event, limit_choices_to={'type': 'EXHIB'},
                              related_name='itineraries', on_delete=models.PROTECT)
    artworks = models.ManyToManyField(Artwork, through='ItineraryArtwork')
    gallery = models.ManyToManyField(
        Gallery, blank=True, related_name='itineraries')

    def __str__(self):
        return '{0} ({1})'.format(self.label_fr, self.event.title)


class ItineraryArtwork(models.Model):
    class Meta:
        ordering = ('order',)
        unique_together = (('itinerary', 'artwork'), ('itinerary', 'order'))

    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
