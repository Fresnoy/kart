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
    mail_sent = send_mail('Le Fresnoy - Candidature completed',
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
    mail_sent = send_mail('Le Fresnoy - Candidature completed',
                          msg_plain,
                          user.email,
                          ['selection@lefresnoy.net'],
                          html_message=msg_html,
                          )

    return mail_sent


def send_candidature_complete_email_to_candidat(request, candidat, application):

    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()

    url = u'{0}{1}'.format(setup.candidatures_url, application.id)
    # Send email
    msg_plain = render_to_string(
        'emails/send_candidature_complete_to_candidat.txt',
        {
            'user': candidat,
            'url': url,
            'application': application
        }
    )
    msg_html = render_to_string(
        'emails/send_candidature_complete_to_candidat.html',
        {
            'user': candidat,
            'url': url,
            'application': application
        }
    )
    mail_sent = send_mail('Le Fresnoy - Candidature complete',
                          msg_plain,
                          'selection@lefresnoy.net',
                          [candidat.email],
                          html_message=msg_html,
                          )

    return mail_sent
