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


class StudentApplication(models.Model):
    """
    Fresnoy's School application procedure
    """
    artist = models.OneToOneField(Artist)

    application_number = models.CharField(editable=False, max_length=50)

    first_time = models.BooleanField(default=True, help_text="If the first time the Artist's applying")
    last_application_year = models.PositiveSmallIntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    remote_interview = models.BooleanField(default=False)
    remote_interview_type = models.CharField(blank=True, max_length=50, help_text="Skype / Gtalk / FaceTime / AppearIn / Other")
    remote_interview_info = models.CharField(blank=True, max_length=50, help_text="ID / Number / ... ")

    administrative_galleries = SortedManyToManyField(Gallery, blank=True, related_name='certificates')
    artwork_galleries = SortedManyToManyField(Gallery, blank=True, related_name='artworks')
