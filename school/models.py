from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from sortedm2m.fields import SortedManyToManyField

from people.models import Artist
from assets.models import Gallery

from datetime import date



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
        return u"{0} ({1}-{2})" % (self.name, self.starting_year, self.ending_year)


class Student(models.Model):
    """
    An artist, part of a promotion, studying for at least 2 years.
    """
    number = models.CharField(max_length=50, null=True, blank=True)
    promotion = models.ForeignKey(Promotion)
    graduate = models.BooleanField(default=False)
    user = models.OneToOneField(User)
    artist = models.OneToOneField(Artist, related_name='student')

    def __unicode__(self):
        return "{0} ({1})".format(self.user, self.number)


class StudentApplication(models.Model):
    """
    Fresnoy's School application procedure
    """
    artist = models.ForeignKey(Artist, related_name='student_application')

    current_year_application_count = models.CharField(max_length=8, default=None, blank=True, help_text=_("Auto generated field (current year - increment number)"))

    first_time = models.BooleanField(default=True, help_text="If the first time the Artist's applying")
    last_application_year = models.PositiveSmallIntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    remote_interview = models.BooleanField(default=False)
    remote_interview_type = models.CharField(blank=True, max_length=50, help_text=_("Skype / Gtalk / FaceTime / AppearIn / Other"))
    remote_interview_info = models.CharField(blank=True, max_length=50, help_text="ID / Number / ... ")

    administrative_galleries = SortedManyToManyField(Gallery, blank=True, related_name='student_application_administrative')
    artwork_galleries = SortedManyToManyField(Gallery, blank=True, related_name='student_application_artwork')

    asynchronous_element = models.BooleanField(default=False, help_text="Element not sent by current form")
    asynchronous_element_description = models.TextField(blank=True, null=True, help_text="What are these elements and how you send it")
    asynchronous_element_received = models.BooleanField(default=False, help_text="Administration - Element have been received")

    remark = models.TextField(blank=True, null=True, help_text="Free expression'")
    application_completed = models.BooleanField(default=False, help_text="Candidature's validation")

    # Administration
    selected_for_interview = models.BooleanField(default=False, help_text="Administration - Is the candidat selected for the Interview")
    selected_for_petit_jury = models.BooleanField(default=False, help_text="Administration - Is the candidat selected for the 'Petit Jury'")
    selected_for_grand_jury = models.BooleanField(default=False, help_text="Administration - Is the candidat selected for the 'Grand Jury'")


    application_complete = models.BooleanField(default=False, help_text="Administration - Candidature is complete")


    def _make_application_number(self):
        """
            Application number algorithm = year + increment_num
        """
        year = date.today().year
        count = StudentApplication.objects.filter(created_on__year=year).count()

        return '{0}-{1:03d}'.format(year,count+1)


    def save(self, *args, **kwargs):
        if not self.current_year_application_count: # self.current_year_application_count == None - wrong condition
            self.current_year_application_count = self._make_application_number()
        super(StudentApplication, self).save(*args, **kwargs)


    def __unicode__(self):
        return "{0} ({1})".format(self.current_year_application_count, self.artist)
