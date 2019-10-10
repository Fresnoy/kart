from django.db.models import Q
from django.db import models
from django_countries.fields import CountryField

from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField

from people.models import User, Organization


class Place(models.Model):
    """
    Some place belonging to an organization
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    address = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=10, blank=True, help_text="Code postal / Zipcode")
    city = models.CharField(max_length=50, blank=True)
    country = CountryField(default="")

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    organization = models.ForeignKey(Organization, blank=True, null=True, related_name='places')

    def __unicode__(self):
        extra_info = self.organization if self.organization else self.country
        address = self.address[0:20]+"..." if self.address else self.city
        return u'{0} - {1} ({2})'.format(self.name, address, extra_info)


def main_event_true():
    from production.models import Event
    return {'pk__in': Event.objects.filter(Q(main_event=True))
                                   .values_list('id', flat=True)}


def main_event_false():
    from production.models import Event
    return {'pk__in': Event.objects.filter(Q(main_event=False))
                                   .values_list('id', flat=True)}


class MetaAward(models.Model):
    """
    Award from main event
    """
    TYPE_CHOICES = (
        ('INDIVIDUAL', 'Individual'),
        ('GROUP', 'Group'),
        ('CAREER', 'Career'),
        ('OTHER', 'Other'),
    )

    label = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    event = models.ForeignKey('production.Event',
                              null=True,
                              limit_choices_to=main_event_true,
                              help_text="Main Event",
                              related_name='meta_award')
    type = models.CharField(max_length=10, null=True, choices=TYPE_CHOICES)
    task = models.ForeignKey('production.StaffTask', blank=True, null=True, related_name='meta_award')

    def __unicode__(self):
        return u'{0} ({2}, cat. {1})'.format(self.label, self.task, self.event)


def staff_and_artist_user_limit():
    return {'pk__in': User.objects.filter(Q(artist__isnull=False) | Q(staff__isnull=False))
                                  .values_list('id', flat=True)}


class Award(models.Model):
    """
    Awards given to artworks & such.
    """
    meta_award = models.ForeignKey(MetaAward, null=True, blank=False, related_name='award')
    artwork = models.ManyToManyField('production.Artwork', blank=True, related_name='award')
    # artist is Artist or Staff
    artist = models.ManyToManyField(User,
                                    blank=True,
                                    limit_choices_to=staff_and_artist_user_limit,
                                    related_name='award',
                                    help_text="Staff or Artist")
    event = models.ForeignKey('production.Event',
                              null=True,
                              blank=False,
                              limit_choices_to=main_event_false,
                              related_name='award')
    ex_aequo = models.BooleanField(default=False)
    giver = models.ManyToManyField(User, blank=True, help_text="Who hands the arward", related_name='give_award')
    sponsor = models.ForeignKey(Organization, null=True, blank=True, related_name='award')
    date = models.DateField(null=True)
    amount = models.CharField(max_length=255, blank=True, help_text="money, visibility, currency free")
    note = models.TextField(blank=True, help_text="Free note")

    def __unicode__(self):
        artworks = ", ".join([artwork.__unicode__() for artwork in self.artwork.all()])
        return u'{0} - {1} pour {2}'.format(self.date.year, self.meta_award, artworks)


class MetaEvent(models.Model):
    """
    Event additionnal Informations
    """
    GENRES_CHOICES = (
        ('FILM', 'Films'),
        ('PERF', 'Performances'),
        ('INST', 'Installations'),
    )
    # Add only one meta to Main Event (primary_key=True)
    event = models.OneToOneField('production.Event',
                                 primary_key=True,
                                 limit_choices_to=main_event_true,
                                 related_name='meta_event')

    genres = MultiSelectField(choices=GENRES_CHOICES, help_text="Global kind of productions shown")
    keywords = TaggableManager(blank=True, help_text="Qualifies Festival: digital arts, residency, electronic festival")
    important = models.BooleanField(default=True, help_text="Helps hide minor events")

    def __unicode__(self):
        return u'{0}'.format(self.event.title)


class Diffusion(models.Model):
    """
    Diffusion additionnal Informations
    """
    FIRST_CHOICES = (
        ('WORLD', 'Mondial'),
        ('INTER', 'International'),
        ('NATIO', 'National'),
    )
    event = models.ForeignKey('production.Event',
                              blank=False,
                              null=False,
                              default=1,
                              limit_choices_to=main_event_false,
                              )
    artwork = models.ForeignKey('production.Artwork', null=False, blank=False, default=1, related_name='diffusion')
    first = models.CharField(max_length=5,
                             blank=True,
                             null=True,
                             choices=FIRST_CHOICES,
                             help_text="Qualifies the first broadcast")
    on_competition = models.BooleanField(default=False, help_text="IN / OFF : On competion or not")

    def __unicode__(self):
        in_or_not = 'IN' if self.on_competition else 'OFF'
        return u'{0} au {1} ({2})'.format(self.artwork.title, self.event.title, in_or_not)

    class Meta:
        # NO DUPLI DIFF
        unique_together = ('id', 'artwork', 'event')
