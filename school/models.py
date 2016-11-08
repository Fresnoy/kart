from django.contrib.auth.models import User
from django.db import models

from people.models import Artist


# Create your models here.
class Promotion(models.Model):
    """
    A promotion of students, for at least 2 years.
    """
    class Meta:
        ordering = ['starting_year']

    name = models.CharField(max_length=255)
    starting_year = models.PositiveSmallIntegerField()
    ending_year = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u"%s (%s-%s)" % (self.name, self.starting_year, self.ending_year)


class Student(models.Model):
    """
    An artist, part of a promotion, studying for at least 2 years.
    """
    number = models.CharField(max_length=50, null=True, blank=True)
    promotion = models.ForeignKey(Promotion)
    graduate = models.BooleanField(default=False)
    user = models.OneToOneField(User)
    artist = models.OneToOneField(Artist)

    def __unicode__(self):
        return "%s (%s)" % (self.user, self.number)
