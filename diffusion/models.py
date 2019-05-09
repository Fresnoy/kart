from django.db.models import Q
from django.db import models
from django_countries.fields import CountryField

from people.models import User, Artist, Organization


class Place(models.Model):
    """
    Some place belonging to an organization
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    address = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=10, blank=True, help_text="Code postal / Zipcode")
    town = models.CharField(max_length=50, blank=True)
    country = CountryField(default="")

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    organization = models.ForeignKey(Organization, blank=True, null=True, related_name='places')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.organization)


class Price(models.Model):
    """
    Price from main event
    """
    TYPE_CHOICES = (
        ('ARTWORK', 'Artwork'),
        ('ARTIST', 'Artist'),
    )

    label = models.CharField(max_length=255)
    description = models.TextField()

    event = models.ForeignKey('production.Event', limit_choices_to=Q(main_event=True), related_name='price')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    task =  models.ForeignKey('production.Task', blank=True, null=True, related_name='price')


class Diffusion(models.Model):
    # ARTWORK
    # Event not main_event
    # premiere (mondiale, international, ville)
    pass


class Award(models.Model):
    """
    Awards given to artworks & such.
    """
    price_label = models.CharField(max_length=255, blank=False, null=True)
    price_description = models.TextField(blank=True)
    mention_label = models.CharField(max_length=255, blank=True)
    mention_description = models.TextField(blank=True)
    artwork = models.ForeignKey('production.Artwork', blank=True, null=True, related_name='award')
    artist = models.ManyToManyField(Artist, blank=True, related_name='award')
    event = models.ForeignKey('production.Event', blank=True, null=True, related_name='award')
    giver = models.ForeignKey(User, blank=True, null=True, help_text="Who hands the prize")
    sponsor = models.ForeignKey(Organization, null=True, blank=True, related_name='award')
    date = models.DateTimeField(null=True)
    amount = models.CharField(max_length=255, blank=True, help_text="money, visibility, currency free")
    note = models.TextField(blank=True, help_text="Free note")
