# -*- coding: utf-8 -*-
import locale
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string

from school.models import StudentApplicationSetup


def send_candidature_completed_email_to_user(request, user, application):
    # Send email
    msg_plain = render_to_string(
        'emails/send_candidature_completed_to_user.txt',
        {
            'application': application
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_completed_to_user.html',
        {
            'application': application
        }
    )
    mail_sent = send_mail('Réception de votre candidature / Application Received',
                          msg_plain,
                          'selection@lefresnoy.net',
                          [user.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_candidature_completed_email_to_admin(request, user, application):

    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()

    url = u'{0}{1}'.format(setup.candidatures_url, application.id)
    # Send email
    msg_plain = render_to_string(
        'emails/send_candidature_completed_to_admin.txt',
        {
            'user': user,
            'url': url,
            'application': application
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_completed_to_admin.html',
        {
            'user': user,
            'url': url,
            'application': application
        }
    )
    mail_sent = send_mail('Envoi d\'une candidature',
                          msg_plain,
                          'selection@lefresnoy.net',
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


def send_candidature_complete_email_to_candidat(request, candidat, application):
    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
    # set locale interviews date
    interviews_dates = {'fr': '', "en": ''}
    setLocale('fr_FR.utf8')
    interviews_dates['fr'] = "du {0} au {1}".format(setup.interviews_start_date.strftime("%A %d %B"),
                                                    setup.interviews_end_date.strftime("%A %d %B %Y")
                                                    )
    setLocale('en_US.utf8')
    interviews_dates['en'] = "from {0} to {1}".format(setup.interviews_start_date.strftime("%A %d %B"),
                                                      setup.interviews_end_date.strftime("%A %d %B %Y")
                                                      )
    setLocale('fr_FR.utf8')
    url = u'{0}{1}'.format(setup.candidatures_url, application.id)
    # Send email
    msg_plain = render_to_string(
        'emails/send_candidature_complete_to_candidat.txt',
        {
            'user': candidat,
            'url': url,
            'application': application,
            'interviews_dates': interviews_dates,
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_complete_to_candidat.html',
        {
            'user': candidat,
            'url': url,
            'application': application,
            'interviews_dates': interviews_dates,
        }
    )
    mail_sent = send_mail('Votre candidature est complète / Candidature is complete',
                          msg_plain,
                          'selection@lefresnoy.net',
                          [candidat.email],
                          html_message=msg_html,
                          )

    return mail_sent


def send_interview_selection_email_to_candidat(request, candidat, application):
    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
    # set locale interviews date
    interview_date = {'fr': '', "en": ''}
    setLocale('fr_FR.utf8')

    interview_date['fr'] = 'Le {0} à {1}'.format(application.interview_date.strftime("%A %d %B %Y"),
                                                 application.interview_date.strftime("%Hh%M")
                                                 )

    setLocale('en_US.utf8')
    interview_date['en'] = "{0}".format(setup.interviews_start_date.strftime("%A %d %B %Y at %H.%M %p"))


    # Send email
    msg_plain = render_to_string(
        'emails/send_interview_selection_to_user.txt',
        {
            'user': candidat,
            'application': application,
            'interview_date': interview_date,
        }
    )
    msg_html = render_to_string(
        'emails/send_interview_selection_to_user.html',
        {
            'user': candidat,
            'application': application,
            'interview_date': interview_date,
        }
    )
    mail_sent = send_mail('Le Fresnoy présélection / preselection',
                          msg_plain,
                          'selection@lefresnoy.net',
                          [candidat.email],
                          html_message=msg_html,
                          )

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

    now = timezone.localtime(timezone.now())
    if (now < campaign.candidature_date_start or
            now > campaign.candidature_date_end):
        return True

    return False
