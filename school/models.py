from django.db import models

from people.models import Artist

# Create your models here.
class Promotion(models.Model):
    """
    A promotion of students, for at least 2 years.
    """
    name = models.CharField(max_length=255)
    starting_year = models.PositiveSmallIntegerField()
    ending_year = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u"%s (%s-%s)" % (self.name, self.starting_year, self.ending_year)

class Student(Artist):
    """
    An artist, part of a promotion, studying for at least 2 years.
    """
    number = models.CharField(max_length=50)
    promotion = models.ForeignKey(Promotion, related_name='students')

    def __unicode__(self):
        return "%s (%s/%s)" % (self.user, self.nickname, self.number)
    