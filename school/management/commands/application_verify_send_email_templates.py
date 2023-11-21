from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.http import HttpRequest

from people.models import Artist
from django.contrib.auth.models import User

from school.utils import (
                    send_activation_email,
                    send_account_information_email,
                    send_candidature_completed_email_to_user,
                    send_candidature_completed_email_to_admin,
                    send_candidature_complete_email_to_candidat,
                    send_interview_selection_email_to_candidat,
                    send_interview_selection_on_waitlist_email_to_candidat,
                    send_selected_candidature_email_to_candidat,
                    send_selected_on_waitlist_candidature_email_to_candidat,
                    send_not_selected_candidature_email_to_candidat,
                    send_candidature_not_finalized_to_candidats,
                    )
from school.models import StudentApplication, AdminStudentApplication, StudentApplicationSetup




def getTemporaryAdminApplication(email):
        user, created = User.objects.get_or_create(username="XXX", email=email)
        artist = Artist.objects.create(user=user)
        campaign = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
        application = StudentApplication.objects.create(artist=artist, campaign=campaign)
        admin_application = AdminStudentApplication.objects.create(application=application)

        return admin_application

def deleteTemporaryAdminApplication(admin_application):
    admin_application.application.artist.user.delete()
    admin_application.application.delete()
    admin_application.delete()


class Command(BaseCommand):
    help = 'Send templates emails for validation'

    def add_arguments(self, parser):
        # -- required
        parser.add_argument("--email", type=str, help='Default : selection@lefresnoy')

    def handle(self, *args, **options):

        email = options['email'] if options['email'] else settings.EMAIL_HOST_USER

        application_admin = getTemporaryAdminApplication(email=email)
        application = application_admin.application

        user = application.artist.user
        user.email = email
        user.activate = False

        request = HttpRequest()
        request.META["SERVER_NAME"] = settings.ALLOWED_HOSTS[0]
        request.META["SERVER_PORT"] = "443"

        send_activation_email(request=request, user=user)
        send_account_information_email(user=user)
        send_candidature_completed_email_to_user(request=request, user=user, application=application)
        send_candidature_completed_email_to_admin(request=request, user=user, application_admin=application_admin)
        send_candidature_complete_email_to_candidat(request=request, candidat=user, application_admin=application_admin)

        # ITW
        application_admin.selected_for_interview = True
        application_admin.interview_date = timezone.now()

        send_interview_selection_email_to_candidat(request=request, candidat=user, application_admin=application_admin)

        # ITW waitlist
        application_admin.wait_listed_for_interview = True
        application_admin.position_in_interview_waitlist = 1

        send_interview_selection_on_waitlist_email_to_candidat(request=request, candidat=user,
                                                               application_admin=application_admin)

        # selected
        application_admin.selected = True
        send_selected_candidature_email_to_candidat(request=request, candidat=user,
                                                    application_admin=application_admin)

        # selected waiting
        application_admin.wait_listed = True
        application_admin.position_in_waitlist = 1

        send_selected_on_waitlist_candidature_email_to_candidat(request=request, candidat=user,
                                                                application_admin=application_admin)

        application_admin.unselected = True
        send_not_selected_candidature_email_to_candidat(request=request, candidat=user,
                                                        application_admin=application_admin)

        application_admin.completed = False
        send_candidature_not_finalized_to_candidats(request=request, application_setup=application.campaign,
                                                    list_candidats=[user.email])
        
        # delete info created
        deleteTemporaryAdminApplication(application_admin)
        
        print("DONE")


