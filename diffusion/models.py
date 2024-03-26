from django.db.models import Q
from django.db import models
from django_countries.fields import CountryField

from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField

from people.models import User, Organization


# TODO: Add field is_city - is_country
class Place(models.Model):
    """
    Some place belonging to an organization
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    address = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(
        max_length=10, blank=True, help_text="Code postal / Zipcode")
    city = models.CharField(max_length=50, blank=True)
    country = CountryField(default="")

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    organization = models.ForeignKey(
        Organization, blank=True, null=True, related_name='places', on_delete=models.CASCADE)

    def __str__(self):
        extra_info = self.organization if self.organization else self.country
        if self.address:
            address = self.address[0:20] + \
                "..." if len(self.address) > 30 else " - " + self.address
        else:
            address = ""

        # Concat with the city
        if self.city:
            address += ", " + self.city

        if not address.lower().find(self.name.lower()):
            return f'{self.name} {self.city} ({extra_info})'
        else:
            return f'{self.name} {address} ({extra_info})'


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
                              limit_choices_to=main_event_true,
                              help_text="Main Event",
                              related_name='meta_award',
                              null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=10, null=True, choices=TYPE_CHOICES)

    task = models.ForeignKey('production.StaffTask',
                             blank=True,
                             null=True,
                             related_name='meta_award',
                             on_delete=models.PROTECT)

    def __str__(self):
        # Removes the "(main event)" description in event representation
        if self.event:
            event = str(self.event)[:-13]
        else:
            event = ''
        if self.task:
            return f'{self.label} ({event}, cat. {self.task})'
        else:
            return f'{self.label} ({event})'


def staff_and_artist_user_limit():
    return {'pk__in': User.objects.filter(Q(artist__isnull=False) | Q(staff__isnull=False))
                                  .values_list('id', flat=True)}


class Award(models.Model):
    """
    Awards given to artworks & such.
    """
    meta_award = models.ForeignKey(
        MetaAward, null=True, blank=False, related_name='award', on_delete=models.PROTECT)
    artwork = models.ManyToManyField(
        'production.Artwork', blank=True, related_name='award')
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
                              related_name='award',
                              on_delete=models.PROTECT)

    ex_aequo = models.BooleanField(default=False)

    giver = models.ManyToManyField(
        User, blank=True, help_text="Who hands the arward", related_name='give_award')

    sponsor = models.ForeignKey(
        Organization, null=True, blank=True, related_name='award', on_delete=models.SET_NULL)

    date = models.DateField(null=True)

    amount = models.CharField(
        max_length=255, blank=True, help_text="money, visibility, currency free")

    note = models.TextField(blank=True, help_text="Free note")

    def __str__(self):
        artworks = ", ".join([artwork.__str__()
                              for artwork in self.artwork.all()])
        return '{0} - {1} pour {2}'.format(self.date.year if self.date else None, self.meta_award, artworks)


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
    # fixMe
    event = models.OneToOneField('production.Event',
                                 primary_key=True,
                                 limit_choices_to=main_event_true,
                                 related_name='meta_event',
                                 on_delete=models.PROTECT
                                 )

    genres = MultiSelectField(choices=GENRES_CHOICES,
                              help_text="Global kind of productions shown")
    keywords = TaggableManager(
        blank=True, help_text="Qualifies Festival: digital arts, residency, electronic festival")
    important = models.BooleanField(
        default=True, help_text="Helps hide minor events")

    def __str__(self):
        return '{0}'.format(self.event.title)


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
                              on_delete=models.PROTECT
                              )

    artwork = models.ForeignKey('production.Artwork',
                                null=False,
                                blank=False,
                                default=1,
                                related_name='diffusion',
                                on_delete=models.PROTECT)

    first = models.CharField(max_length=5,
                             blank=True,
                             null=True,
                             choices=FIRST_CHOICES,
                             help_text="Qualifies the first broadcast")

    on_competition = models.BooleanField(
        default=False, help_text="IN / OFF : On competion or not")

    def __str__(self):
        in_or_not = 'IN' if self.on_competition else 'OFF'
        return '{0} au {1} ({2})'.format(self.artwork.title, self.event.title, in_or_not)

    class Meta:
        # NO DUPLI DIFF
        unique_together = ('id', 'artwork', 'event')
