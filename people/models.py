from django.contrib.auth.models import User
from django.db import models

from django_countries.fields import CountryField


class FresnoyProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    photo = models.ImageField(upload_to="user_photos")
    
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=255)
    birthplace_country = CountryField()

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
    website = models.URLField(blank=True)
    
    def __unicode__(self):    
        return u"%s (%s)" % (self.user, self.nickname)

class Staff(models.Model):
    """
    Someone working at Le Fresnoy (insider) or for a production
    """
    user = models.ForeignKey(User)
