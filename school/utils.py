# -*- coding: utf-8 -*-
import locale
import pytz

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from school.models import StudentApplicationSetup


def send_activation_email(request, user):

    # Create activation token URL
    uidb64 = int_to_base36(user.id)
    token = default_token_generator.make_token(user)
    url = reverse('candidat-activate', kwargs={
        'uidb64': uidb64,
        'token': token,
    })
    absolute_url = request.build_absolute_uri(url)
    # Send email
    msg_plain = render_to_string('emails/account/send_activation_link.txt', {'url': absolute_url})
    msg_html = render_to_string('emails/account/send_activation_link.html', {'url': absolute_url})

    mail_sent = send_mail('Confirmez la création de votre compte',
                          msg_plain,
                          settings.FROM_EMAIL,
                          [user.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_account_information_email(user):

    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()

    recover_password_url = setup.recover_password_url
    authentification_url = setup.authentification_url

    # Send email
    msg_plain = render_to_string('emails/account/account_infos.txt', {
                                 'user': user,
                                 'recover_password_url': recover_password_url,
                                 'authentification_url': authentification_url
                                 })
    msg_html = render_to_string('emails/account/account_infos.html', {
                                'user': user,
                                'recover_password_url': recover_password_url,
                                'authentification_url': authentification_url
                                })
    mail_sent = send_mail('Résumé de votre compte / Account information',
                          msg_plain,
                          settings.FROM_EMAIL,
                          [user.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_candidature_completed_email_to_user(request, user, application):
    # Send email
    msg_plain = render_to_string(
        'emails/send_candidature_completed_to_user.txt',
        {
            'user': user,
            'application': application
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_completed_to_user.html',
        {
            'user': user,
            'application': application
        }
    )
    mail_sent = send_mail('Réception de votre candidature / Application Received',
                          msg_plain,
                          settings.FROM_EMAIL,
                          [user.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_candidature_completed_email_to_admin(request, user, application_admin):

    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()

    url = '{0}{1}'.format(setup.candidatures_url, application_admin.id)
    # Send email
    msg_plain = render_to_string(
        'emails/send_candidature_completed_to_admin.txt',
        {
            'user': user,
            'url': url,
            'application': application_admin.application
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_completed_to_admin.html',
        {
            'user': user,
            'url': url,
            'application': application_admin.application
        }
    )
    mail_sent = send_mail('Envoi d\'une candidature',
                          msg_plain,
                          settings.FROM_EMAIL,
                          ['selection@lefresnoy.net'],
                          html_message=msg_html,
                          )

    return mail_sent


def setLocale(str):
    # windows translation
    dict = {'fr_FR.utf8': 'french', 'en_US.utf8': 'english'}
    try:
        locale.setlocale(locale.LC_ALL, str)
    except Exception:
        locale.setlocale(locale.LC_ALL, dict[str])


def send_candidature_complete_email_to_candidat(request, candidat, application_admin):
    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
    # set locale  interviews date
    interviews_dates = {'fr': '', "en": ''}
    # having name of day/month in rigth language
    setLocale('fr_FR.utf8')
    interviews_dates['fr'] = "du {0} au {1}".format(setup.interviews_start_date.strftime("%A %d %B"),
                                                    setup.interviews_end_date.strftime("%A %d %B %Y")
                                                    )
    setLocale('en_US.utf8')
    interviews_dates['en'] = "from {0} to {1}".format(setup.interviews_start_date.strftime("%A %d %B"),
                                                      setup.interviews_end_date.strftime("%A %d %B %Y")
                                                      )
    setLocale('fr_FR.utf8')
    # Send email
    msg_plain = render_to_string(
        'emails/send_candidature_complete_to_candidat.txt',
        {
            'user': candidat,
            'interviews_dates': interviews_dates,
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_complete_to_candidat.html',
        {
            'user': candidat,
            'interviews_dates': interviews_dates,
        }
    )
    mail_sent = send_mail('Votre candidature est complète / Candidature is complete',
                          msg_plain,
                          settings.FROM_EMAIL,
                          [candidat.email],
                          html_message=msg_html,
                          )

    return mail_sent


def send_interview_selection_email_to_candidat(request, candidat, application_admin):
    # set var for email template
    interview_date = {'fr': '', "en": ''}
    # set locale interviews date
    # having name of day/month in rigth language
    setLocale('fr_FR.utf8')
    # convert utc to PARIS's time
    tz = pytz.timezone("Europe/Paris")
    interview_date_paris = application_admin.interview_date.astimezone(tz)
    # get French string date : lundi 01 juillet 2019 à 13h30
    interview_date['fr'] = 'Le {0} à {1}'.format(
        interview_date_paris.strftime("%A %d %B %Y"),
        interview_date_paris.strftime("%Hh%M")
    )
    setLocale('en_US.utf8')
    # get English string date : monday 01 july 2019 à 01h30 PM
    interview_date['en'] = "{0}".format(
        interview_date_paris.strftime("%A %d %B %Y at %I.%M %p")
    )
    # Send email
    msg_plain = render_to_string(
        'emails/send_interview_selection_to_user.txt',
        {
            'user': candidat,
            'interview_date': interview_date,
        }
    )
    msg_html = render_to_string(
        'emails/send_interview_selection_to_user.html',
        {
            'user': candidat,
            'interview_date': interview_date,
        }
    )
    mail_sent = send_mail('Le Fresnoy présélection / preselection',
                          msg_plain,
                          settings.FROM_EMAIL,
                          [candidat.email],
                          html_message=msg_html,
                          )

    return mail_sent


def send_interview_selection_on_waitlist_email_to_candidat(request, candidat, application_admin):
    # set locale  interviews date
    interviews_dates = {'fr': '', "en": ''}
    # having name of day/month in rigth language
    setLocale('fr_FR.utf8')
    setup = application_admin.application.campaign
    interviews_dates['fr'] = "entre le {0} au {1}".format(setup.interviews_start_date.strftime("%A %d %B"),
                                                          setup.interviews_end_date.strftime("%A %d %B %Y")
                                                          )
    setLocale('en_US.utf8')
    interviews_dates['en'] = "from {0} to {1}".format(setup.interviews_start_date.strftime("%A %d %B"),
                                                      setup.interviews_end_date.strftime("%A %d %B %Y")
                                                      )

    # Send email : PRESELECTION : ON WAITLIST
    msg_plain = render_to_string(
        'emails/send_on_waitlist_for_interview_to_candidat.txt',
        {
            'application_admin': application_admin,
            'user': candidat,
            'interviews_dates': interviews_dates
        }
    )
    msg_html = render_to_string(
        'emails/send_on_waitlist_for_interview_to_candidat.html',
        {
            'application_admin': application_admin,
            'user': candidat,
            'interviews_dates': interviews_dates
        }
    )
    mail_sent = send_mail('Candidature | Le Fresnoy – Studio national des arts contemporains',
                          msg_plain,
                          settings.FROM_EMAIL,
                          [candidat.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_selected_candidature_email_to_candidat(request, candidat, application_admin):
    # Send email : SELECTED
    msg_plain = render_to_string(
        'emails/send_selected_email_to_candidat.txt',
        {
            'user': candidat,
        }
    )
    msg_html = render_to_string(
        'emails/send_selected_email_to_candidat.html',
        {
            'user': candidat,
        }
    )
    subject = 'Candidature | Le Fresnoy – Studio national des arts contemporains '

    mail_sent = send_mail(subject,
                          msg_plain,
                          settings.FROM_EMAIL,
                          [candidat.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_selected_on_waitlist_candidature_email_to_candidat(request, candidat, application_admin):
    # Send email : SELECTED IN WAITLIST
    msg_plain = render_to_string(
        'emails/send_on_waitlist_for_selection_to_candidat.txt',
        {
            'application_admin': application_admin,
            'user': candidat,
        }
    )
    msg_html = render_to_string(
        'emails/send_on_waitlist_for_selection_to_candidat.html',
        {
            'application_admin': application_admin,
            'user': candidat,
        }
    )
    subject = 'Candidature | Le Fresnoy – Studio national des arts contemporains '

    mail_sent = send_mail(subject,
                          msg_plain,
                          settings.FROM_EMAIL,
                          [candidat.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_not_selected_candidature_email_to_candidat(request, candidat, application_admin):
    # Send email : NOT SELECTED
    msg_plain = render_to_string(
        'emails/send_not_selected_email_to_candidat.txt',
        {
            'application': application_admin.application,
            'user': candidat,
        }
    )
    msg_html = render_to_string(
        'emails/send_not_selected_email_to_candidat.html',
        {
            'application': application_admin.application,
            'user': candidat,
        }
    )
    subject = 'Candidature | Le Fresnoy – Studio national des arts contemporains '

    mail_sent = send_mail(subject,
                          msg_plain,
                          settings.FROM_EMAIL,
                          [candidat.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_candidature_not_finalized_to_candidats(request, application_setup, list_candidats):

    # set locale  interviews date
    application_end = {'fr': '', "en": ''}
    # having name of day/month in rigth language
    setLocale('fr_FR.utf8')
    tz = pytz.timezone("Europe/Paris")
    candidature_date_end = application_setup.candidature_date_end.astimezone(tz)

    application_end['fr'] = '{0} à {1}'.format(
        candidature_date_end.strftime("%A %d %B %Y"),
        candidature_date_end.strftime("%Hh%M")
    )
    setLocale('en_US.utf8')
    application_end['en'] = candidature_date_end.strftime("%I %p/%H.%M (Paris time) on %A %d %B %Y")
    # Send email : NOT SELECTED
    msg_plain = render_to_string(
        'emails/send_candidature_not_finalized_to_candidat.txt',
        {
            'application_end': application_end
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_not_finalized_to_candidat.html',
        {
            'application_end': application_end
        }
    )
    mail = EmailMultiAlternatives('Finalisez votre candidature / Finalize your application ',
                                  msg_plain,
                                  settings.FROM_EMAIL,
                                  ['selection@lefresnoy.net', ],
                                  bcc=list_candidats,  # bcc
                                  reply_to=['selection@lefresnoy.net'],
                                  )
    mail.attach_alternative(msg_html, "text/html")
    mail_sent = mail.send()
    return mail_sent


def candidature_close(campaign=None):
    """
    Test if a candidature is closed
    """
    # Try to get current campaign
    if not campaign:
        campaign = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
    if not campaign:
        return False

    # is candidature on time
    now = timezone.localtime(timezone.now())
    if (now < campaign.candidature_date_start or
            now > campaign.candidature_date_end):
        return True

    return False
