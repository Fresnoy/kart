from django.core.mail import send_mail
from django.template.loader import render_to_string

from ifresnoy.settings import front_candidatures_url


def send_candidature_completed_email_to_user(request, user):
    # Send email
    msg_plain = render_to_string('emails/send_candidature_completed_to_user.txt')
    msg_html = render_to_string('emails/send_candidature_completed_to_user.html')

    mail_sent = send_mail('Le Fresnoy - Candidature completed',
                          msg_plain,
                          'pedagogie@lefresnoy.net',
                          [user.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_candidature_completed_email_to_admin(request, user, application_id):

    url = u'{0}{1}'.format(front_candidatures_url, application_id)
    # Send email
    msg_plain = render_to_string('emails/send_candidature_completed_to_admin.txt', {'user': user, 'url': url})
    msg_html = render_to_string('emails/send_candidature_completed_to_admin.html', {'user': user, 'url': url})

    mail_sent = send_mail('Le Fresnoy - Candidature completed',
                          msg_plain,
                          user.email,
                          ['pedagogie@lefresnoy.net'],
                          html_message=msg_html,
                          )

    return mail_sent
