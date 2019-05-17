from django.db.models import Q
from django.db import models
from django_countries.fields import CountryField

from people.models import User, Organization


class Place(models.Model):
    """
    Some place belonging to an organization
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    address = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=10, blank=True, help_text="Code postal / Zipcode")
    town = models.CharField(max_length=50, blank=True)
    country = CountryField(default="")

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    organization = models.ForeignKey(Organization, blank=True, null=True, related_name='places')

    def __unicode__(self):
        extra_info = self.organization if self.organization else self.country
        return u'{0} ({1})'.format(self.name, extra_info)


class Award(models.Model):
    """
    Award from main event
    """
    TYPE_CHOICES = (
        ('ARTWORK', 'Artwork'),
        ('ARTIST', 'Artist'),
    )

    label = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    event = models.ForeignKey('production.Event',
                              null=True,
                              limit_choices_to=Q(main_event=True),
                              help_text="Main Event",
                              related_name='award')
    type = models.CharField(max_length=10, null=True, choices=TYPE_CHOICES)
    task = models.ForeignKey('production.StaffTask', blank=True, null=True, related_name='award')

    def __unicode__(self):
        return u'{0} ({2}, cat. {1})'.format(self.label, self.task, self.event)


class Diffusion(models.Model):
    # ARTWORK
    # Event not main_event
    # premiere (mondiale, international, ville)
    pass


class Reward(models.Model):
    """
    Awards given to artworks & such.
    """
    # price_label = models.CharField(max_length=255, blank=False, null=True)
    # price_description = models.TextField(blank=True)
    # mention_label = models.CharField(max_length=255, blank=True)
    # mention_description = models.TextField(blank=True)
    # artist = models.ManyToManyField(Artist, blank=True, related_name='award')
    award = models.ForeignKey(Award, related_name='reward')
    artwork = models.ForeignKey('production.Artwork', related_name='rewards')
    event = models.ForeignKey('production.Event', limit_choices_to=Q(main_event=False), related_name='reward')
    giver = models.ForeignKey(User, blank=True, null=True, help_text="Who hands the prize")
    sponsor = models.ForeignKey(Organization, null=True, blank=True, related_name='reward')
    date = models.DateField(null=True)
    amount = models.CharField(max_length=255, blank=True, help_text="money, visibility, currency free")
    note = models.TextField(blank=True, help_text="Free note")

    def __unicode__(self):
        return u'{0} pour {1}'.format(self.award, self.artwork)
