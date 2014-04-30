from django.contrib.auth.models import User
from django.db import models

from django_countries.fields import CountryField

from common.models import Website
from common.utils import make_filepath

class FresnoyProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    photo = models.ImageField(upload_to=make_filepath)
    
    birthdate = models.DateField(null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    birthplace_country = CountryField(null=True, blank=True)

    homeland_address = models.TextField(blank=True)
    homeland_country = CountryField(blank=True)
    residence_address = models.TextField(blank=True)
    residence_country = CountryField(blank=True)

    homeland_phone = models.CharField(max_length=50, blank=True)
    residence_phone = models.CharField(max_length=50, blank=True)

    cursus = models.TextField(blank=True)


class Artist(models.Model):
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=255, blank=True)
    bio_short_fr = models.TextField(blank=True)
    bio_short_en = models.TextField(blank=True)
    bio_fr = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)

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

    def __unicode__(self):
        return self.user.username

class Organization(models.Model):
    """
    An org 
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to=make_filepath, blank=True)

    def __unicode__(self):
        return self.name