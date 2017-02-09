from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36

from school.models import StudentApplicationSetup


def send_activation_email(request, user):

    # Create activation token URL
    uidb36 = int_to_base36(user.id)
    token = default_token_generator.make_token(user)
    url = reverse('user-activate', kwargs={
        'uidb36': uidb36,
        'token': token,
    })
    absolute_url = request.build_absolute_uri(url)
    # Send email
    msg_plain = render_to_string('emails/send_activation_link.txt', {'url': absolute_url})
    msg_html = render_to_string('emails/send_activation_link.html', {'url': absolute_url})

    mail_sent = send_mail('Le Fresnoy - Activation du compte',
                          msg_plain,
                          'pedagogie@lefresnoy.net',
                          [user.email],
                          html_message=msg_html,
                          )
    return mail_sent


def send_account_information_email(user):

    setup = StudentApplicationSetup.objects.filter(is_current_setup=True).first()

    recover_password_url = setup.recover_password_url
    authentification_url = setup.authentification_url

    # Send email
    msg_plain = render_to_string('emails/account_infos.txt', {
                                 'user': user,
                                 'recover_password_url': recover_password_url,
                                 'authentification_url': authentification_url
                                 })
    msg_html = render_to_string('emails/account_infos.html', {
                                'user': user,
                                'recover_password_url': recover_password_url,
                                'authentification_url': authentification_url
                                })
    mail_sent = send_mail('Le Fresnoy - Activation du compte',
                          msg_plain,
                          'poleweb@lefresnoy.net',
                          [user.email],
                          html_message=msg_html,
                          )
    return mail_sent
