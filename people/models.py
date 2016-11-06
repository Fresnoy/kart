from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField

from django_countries.fields import CountryField
from polymorphic.models import PolymorphicModel
from django_languages.fields import LanguageField

from common.models import Website
from common.utils import make_filepath



class FresnoyProfile(models.Model):

    GENDER_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female'),
            ('T', 'Transgender'),
            ('O', 'Other'),
        )


    user = models.OneToOneField(User, related_name='profile')
    photo = models.ImageField(upload_to=make_filepath, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=False)

    birthdate = models.DateField(null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    birthplace_country = CountryField(null=True, blank=True)

    homeland_address = models.TextField(blank=True)
    homeland_country = CountryField(blank=True)
    residence_address = models.TextField(blank=True)
    residence_country = CountryField(blank=True)

    homeland_phone = models.CharField(max_length=50, blank=True)
    residence_phone = models.CharField(max_length=50, blank=True)

    FAMILY_STATUS_CHOICES = (
        ("S", "Single"),
        ("E", "Engaged"),
        ("M", "Married"),
        ("D", "Divorced"),
        ("W", "Widowed"),
        ("C", "Civil Union"),
    )

    social_insurance_number = models.CharField(max_length=50, blank=True)
    family_status = models.CharField(max_length=1,
                                     choices=FAMILY_STATUS_CHOICES,
                                     null=True, blank=True)

    mother_tongue = LanguageField(blank=True, null=True)
    other_language = LanguageField(blank=True, null=True)

    cursus = models.TextField(blank=True)


class Artist(models.Model):
    class Meta:
        ordering = ['user__last_name']

    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=255, blank=True)
    bio_short_fr = models.TextField(blank=True)
    bio_short_en = models.TextField(blank=True)
    bio_fr = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)

    updated_on = models.DateTimeField(auto_now=True)

    twitter_account = models.CharField(max_length=100, blank=True)
    facebook_profile = models.URLField(blank=True)
    websites = models.ManyToManyField(Website, blank=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.user, self.nickname)

class Staff(models.Model):
    """
    Someone working at Le Fresnoy (insider) or for a production
    """
    user = models.ForeignKey(User)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

class Organization(models.Model):
    """
    An org
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to=make_filepath, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
