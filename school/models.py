from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from common.utils import make_filepath
from people.models import Artist, Organization
from assets.models import Gallery
from production.models import Artwork


class Promotion(models.Model):
    """
    A promotion of students, for at least 2 years.
    """
    class Meta:
        ordering = ['starting_year']

    name = models.CharField(max_length=255)
    starting_year = models.PositiveSmallIntegerField()
    ending_year = models.PositiveSmallIntegerField()
    picture = models.ImageField(upload_to=make_filepath, blank=True)

    def __str__(self):
        return '{0} ({1}-{2})'.format(self.name, self.starting_year, self.ending_year)


class Student(models.Model):
    """
    An artist, part of a promotion, studying for at least 2 years.
    """
    number = models.CharField(max_length=50, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, null=True, on_delete=models.SET_NULL)
    graduate = models.BooleanField(default=False)
    mention = models.TextField(null=True, blank=True, help_text="Mention")
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    artist = models.OneToOneField(Artist, related_name='student', on_delete=models.PROTECT)

    def __str__(self):
        return '{0} ({1})'.format(self.user, self.number)


class TeachingArtist(models.Model):
    """
    An artist accompany a student for artwork
    """
    artist = models.OneToOneField(Artist, related_name='teacher', null=True, on_delete=models.SET_NULL)
    presentation_text_fr = models.TextField(null=True,
                                            blank=True,
                                            help_text="General orientation text (not only bio) in FRENCH"
                                            )
    presentation_text_en = models.TextField(null=True,
                                            blank=True,
                                            help_text="General orientation text (not only bio) in ENGLISH"
                                            )
    pictures_gallery = models.OneToOneField(
        Gallery, blank=True, null=True, related_name='teachingartist_pictures', on_delete=models.CASCADE)
    artworks_supervision = models.ManyToManyField(Artwork, related_name='mentoring', blank=True)

    def __str__(self):
        return '{0}'.format(self.artist)


class ScienceStudent(models.Model):
    """
    An scientific with a discipline, studying at least one year and make artwork.
    """
    student = models.OneToOneField(Student, related_name='science_student', on_delete=models.PROTECT)
    discipline = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.student)


class PhdStudent(models.Model):
    """
    An Phd student follows the course in 3 years and produces a thesis
    """
    student = models.OneToOneField(Student, related_name='phd_student', on_delete=models.PROTECT)
    university = models.ForeignKey(Organization, related_name='phd_student', on_delete=models.PROTECT, blank=True)
    director = models.ForeignKey(User, related_name='phd_student', on_delete=models.PROTECT, blank=True)
    thesis_object = models.CharField(max_length=150, null=True, blank=True)
    thesis_file = models.FileField(upload_to=make_filepath, null=True, blank=True, help_text="thesis pdf file")

    def __str__(self):
        return '{0}'.format(self.student)


class StudentApplicationSetup(models.Model):
    """
    Setup Student Application
    """
    name = models.CharField(max_length=25, null=True, blank=True)
    # Promo
    promotion = models.ForeignKey(Promotion, null=True, blank=False, on_delete=models.SET_NULL)
    # date
    candidature_date_start = models.DateTimeField(null=False, blank=False)
    candidature_date_end = models.DateTimeField(null=False, blank=False)
    # front text
    interviews_start_date = models.DateField(null=True, blank=False, help_text="Front : interviews start date")
    interviews_end_date = models.DateField(null=True, blank=False, help_text="Front : interviews end date")
    date_of_birth_max = models.DateField(null=True, blank=True, help_text="Maximum date of birth to apply")
    # Publications's date
    interviews_publish_date = models.DateTimeField(null=True, blank=False, help_text="Interviews web publish")
    selected_publish_date = models.DateTimeField(null=True, blank=False, help_text="Final selection web publish")
    # front auth
    candidatures_url = models.URLField(null=False, blank=False, help_text="Front : Url list of candidatures")
    reset_password_url = models.URLField(null=False, blank=False, help_text="Front : Url reset password")
    recover_password_url = models.URLField(null=False, blank=False, help_text="Front : Url recover password")
    authentification_url = models.URLField(null=False, blank=False, help_text="Front : Url authentification")
    # vimeo
    video_service_name = models.CharField(max_length=25, null=True, blank=True, help_text="video service name")
    video_service_url = models.URLField(null=False, blank=False, help_text="service URL")
    video_service_token = models.CharField(max_length=128, null=True, blank=True, help_text="Video service token")
    # current setup
    is_current_setup = models.BooleanField(
        default=True,
        help_text="This configuration is actived"
    )

    def _make_default_birthdate_max(self):
        """
            31 december currentyear or next promo year minus 36
        """
        max_age = 36
        current_year = date.today().year
        # current_year is the next promo start year if exist
        campaign = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
        if campaign:
            current_year = int(campaign.promotion.starting_year)
        return date(current_year-max_age, 12, 31)

    def save(self, *args, **kwargs):
        # set default date of birth max (calulated)
        if not self.date_of_birth_max:
            self.date_of_birth_max = self._make_default_birthdate_max()
        # set all current setups to False
        # TODO : only one current setup can be true
        if self.is_current_setup:
            StudentApplicationSetup.objects.filter(is_current_setup=True).update(is_current_setup=False)

        super(StudentApplicationSetup, self).save(*args, **kwargs)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.promotion.name)


class StudentApplication(models.Model):
    """
    Fresnoy's School application procedure
    """
    artist = models.ForeignKey(Artist, related_name='student_application', null=True, on_delete=models.SET_NULL)
    campaign = models.ForeignKey(StudentApplicationSetup, blank=True, related_name='applications',
                                 null=True, on_delete=models.SET_NULL)

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
    INE = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text="Identifiant National Etudiant (only French student) - 10 numbers + 1 letter ou 9 numbers + 2 letters"
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
        max_length=10,
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
        help_text='Gallery of justificaitons',
        on_delete=models.PROTECT
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
    interview_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Administration - Date for interview"
    )
    wait_listed_for_interview = models.BooleanField(
        default=False,
        help_text="Administration - Is the candidat wait listed for the Interview"
    )
    position_in_interview_waitlist = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Administration - Set the position in interview waitlist"
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
    position_in_waitlist = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Administration - Set the position in waitlist"
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
        # settup app number with current campaign promo if exist
        campaign = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
        if campaign:
            year = campaign.promotion.starting_year
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

    def __str__(self):
        return "{0} ({1})".format(self.current_year_application_count, self.artist)
