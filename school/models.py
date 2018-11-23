from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from common.utils import make_filepath
from people.models import Artist
from assets.models import Gallery


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
        return u'{0} ({1}-{2})'.format(self.name, self.starting_year, self.ending_year)


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
        return u'{0} ({1})'.format(self.user, self.number)


class StudentApplicationSetup(models.Model):
    """
    Setup Student Apllication
    """
    name = models.CharField(max_length=25, null=True, blank=True)
    # Promo
    promotion = models.ForeignKey(Promotion, null=False, blank=False)
    # date
    candidature_date_start = models.DateField(null=False, blank=False)
    candidature_date_end = models.DateField(null=False, blank=False)
    # Publications's date
    interviews_publish_date = models.DateField(null=True, blank=False, help_text="Interviews web publish")
    selected_publish_date = models.DateField(null=True, blank=False, help_text="Final selection web publish")
    # front
    candidatures_url = models.URLField(null=False, blank=False, help_text="Front : Url list of candidatures")
    reset_password_url = models.URLField(null=False, blank=False, help_text="Front : Url reset password")
    recover_password_url = models.URLField(null=False, blank=False, help_text="Front : Url recover password")
    authentification_url = models.URLField(null=False, blank=False, help_text="Front : Url authentification")
    # front text
    interviews_start_date = models.DateField(null=True, blank=False, help_text="Front : interviews start date")
    interviews_end_date = models.DateField(null=True, blank=False, help_text="Front : interviews end date")
    # vimeo
    video_service_name = models.CharField(max_length=25, null=True, blank=True, help_text="video service name")
    video_service_url = models.URLField(null=False, blank=False, help_text="service URL")
    video_service_token = models.CharField(max_length=128, null=True, blank=True, help_text="Video service token")
    # vimeo
    is_current_setup = models.BooleanField(
        default=True,
        help_text="This configuration is actived"
    )

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.promotion.name)


class StudentApplication(models.Model):
    """
    Fresnoy's School application procedure
    """
    artist = models.ForeignKey(Artist, related_name='student_application')
    campain = models.ForeignKey(StudentApplicationSetup, blank=True, null=True, related_name='applications')

    current_year_application_count = models.CharField(
        max_length=8,
        default=None,
        blank=True,
        help_text=_("Auto generated field (current year - increment number)")
    )

    identity_card = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Identity justificative"
    )
    # First Candidature
    first_time = models.BooleanField(
        default=False,
        help_text="If the first time the Artist's applying"
    )
    last_applications_years = models.CharField(
        blank=True,
        max_length=50,
        help_text=_("Already candidate")
    )
    # Dates of creation
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Interview type
    remote_interview = models.BooleanField(default=False)
    remote_interview_type = models.CharField(
        blank=True,
        max_length=50,
        help_text=_("Skype / Gtalk / FaceTime / AppearIn / Other")
    )
    remote_interview_info = models.CharField(
        blank=True,
        max_length=50,
        help_text="ID / Number / ... "
    )
    # Master Degree
    master_degree = models.CharField(
        max_length=1,
        choices=(('Y', 'Yes'), ('N', 'No'), ('P', 'Pending'),),
        null=True,
        blank=True,
        help_text="Obtained a Master Degree"
    )
    experience_justification = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="If no master Degree, experience letter"
    )
    # Cursus
    cursus_justifications = models.ForeignKey(
        Gallery,
        blank=True,
        null=True,
        related_name='student_application_cursus_justification',
        help_text='Gallery of justificaitons'
    )
    curriculum_vitae = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="BIO CV"
    )
    justification_letter = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Justification / Motivation"
    )
    reference_letter = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Reference / Recommendation letter"
    )
    free_document = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Free document"
    )
    # candidature duo
    binomial_application = models.BooleanField(
        default=False,
        help_text="Candidature with another artist"
    )
    binomial_application_with = models.CharField(
        blank=True,
        max_length=50,
        help_text="Name of the binominal artist's candidate with"
    )
    # first and second year project
    considered_project_1 = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Considered project first year"
    )
    artistic_referencies_project_1 = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Artistic references for first first year's project"
    )
    considered_project_2 = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Considered project second year"
    )
    artistic_referencies_project_2 = models.FileField(
        upload_to=make_filepath,
        null=True,
        blank=True,
        help_text="Artistic references for second first year's project"
    )
    doctorate_interest = models.BooleanField(
        default=False,
        help_text="Interest in the doctorate"
    )
    # Video
    presentation_video = models.URLField(
        null=True,
        blank=True,
        help_text="Url presentation video Link"
    )
    presentation_video_details = models.TextField(
        null=True,
        blank=True,
        help_text="Details for the video"
    )
    presentation_video_password = models.CharField(
        blank=True,
        max_length=50,
        help_text=_("Password for the video")
    )
    remark = models.TextField(blank=True, null=True, help_text="Free expression'")
    application_completed = models.BooleanField(
        default=False,
        help_text="Candidature's validation"
    )
    # Administration
    observation = models.TextField(blank=True, null=True, help_text="Administration - Comments on the application")

    selected_for_interview = models.BooleanField(
        default=False,
        help_text="Administration - Is the candidat selected for the Interview"
    )
    interview_date = models.DateField(
        null=True,
        blank=True,
        help_text="Administration - Date for interview"
    )
    wait_listed_for_interview = models.BooleanField(
        default=False,
        help_text="Administration - Is the candidat wait listed for the Interview"
    )
    selected = models.BooleanField(
        default=False,
        help_text="Administration - Is the candidat selected"
    )
    unselected = models.BooleanField(
        default=False,
        help_text="Administration - Is the candidat not choosen by the Jury"
    )
    wait_listed = models.BooleanField(
        default=False,
        help_text="Administration - Is the candidat wait listed"
    )
    application_complete = models.BooleanField(
        default=False,
        help_text="Administration - Candidature is complete"
    )

    def _make_application_number(self):
        """
            Application number algorithm = year + increment_num
        """
        year = date.today().year
        carry_on = True
        default_number = 103
        inc = 0
        while carry_on:
            inc += 1
            application_number = '{0}-{1:03d}'.format(year, default_number + inc)
            carry_on = StudentApplication.objects.filter(current_year_application_count=application_number).exists()

        return application_number

    def save(self, *args, **kwargs):

        if not self.current_year_application_count:
            self.current_year_application_count = self._make_application_number()

        super(StudentApplication, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{0} ({1})".format(self.current_year_application_count, self.artist)
