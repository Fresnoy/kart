from django.db import models
from django.contrib.auth.models import User


from django_countries.fields import CountryField
from languages.fields import LanguageField

from common.utils import make_filepath

from common.models import Website


class FresnoyProfile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=make_filepath, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    nationality = models.CharField(max_length=24, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    birthplace = models.CharField(max_length=255, null=True, blank=True)
    birthplace_country = CountryField(null=True, default="")

    homeland_address = models.TextField(blank=True)
    homeland_zipcode = models.CharField(max_length=10, blank=True)
    homeland_town = models.CharField(max_length=50, blank=True)
    homeland_country = CountryField(default="")
    residence_address = models.TextField(blank=True)
    residence_zipcode = models.CharField(max_length=10, blank=True)
    residence_town = models.CharField(max_length=50, blank=True)
    residence_country = CountryField(default="")

    homeland_phone = models.CharField(max_length=50, blank=True)
    residence_phone = models.CharField(max_length=50, blank=True)

    social_insurance_number = models.CharField(max_length=50, blank=True)
    family_status = models.CharField(max_length=50,
                                     null=True, blank=True)

    mother_tongue = LanguageField(blank=True, null=True)
    other_language = models.CharField(max_length=24, null=True, blank=True)

    cursus = models.TextField(blank=True)

    def __str__(self):
        return 'Profile {}'.format(self.user)

    @property
    def is_artist(self):
        return self.user.artist_set.count() > 0

    def is_staff(self):
        return self.user.staff_set.count() > 0

    def is_student(self):
        return hasattr(self.user, 'student')


class Artist(models.Model):
    class Meta:
        ordering = ['user__last_name']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255, blank=True)
    bio_short_fr = models.TextField(blank=True)
    bio_short_en = models.TextField(blank=True)
    bio_fr = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)

    updated_on = models.DateTimeField(auto_now=True)

    twitter_account = models.CharField(max_length=100, blank=True)
    facebook_profile = models.URLField(blank=True)
    websites = models.ManyToManyField(Website, blank=True)

    def __str__(self):
        return '{}'.format(self.nickname) if self.nickname else "{} {}".format(self.user.first_name,
                                                                               self.user.last_name)


class Staff(models.Model):
    """
    Someone working at Le Fresnoy (insider) or for a production
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.user)

    class Meta:
        ordering = ['user__first_name']


class Organization(models.Model):
    """
    An organisation
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to=make_filepath, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
