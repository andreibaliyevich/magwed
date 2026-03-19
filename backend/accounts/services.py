from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .utilities import encode_uid, make_token


def send_activation_email(user, lang_code):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'LANG_CODE': lang_code,
        'uid': encode_uid(user.uuid),
        'token': make_token(user),
    }

    subject = render_to_string('email/activation_subject.txt')
    text_content = render_to_string('email/activation_text.html', context)
    html_content = render_to_string('email/activation_html.html', context)

    user.email_user(
        subject=subject,
        message=text_content,
        from_email=settings.EMAIL_HOST_USER,
        html_message=html_content,
    )


def send_password_reset_email(user, lang_code):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_HOST': settings.SITE_HOST,
        'LANG_CODE': lang_code,
        'uid': encode_uid(user.uuid),
        'token': make_token(user),
    }

    subject = render_to_string('email/password_reset_subject.txt')
    text_content = render_to_string(
        'email/password_reset_text.html', context)
    html_content = render_to_string(
        'email/password_reset_html.html', context)

    user.email_user(
        subject=subject,
        message=text_content,
        from_email=settings.EMAIL_HOST_USER,
        html_message=html_content,
    )


def check_pro_account(user):
    """ Check user is a professional account """
    if timezone.now() < user.organizer.pro_time:
        return True
    else:
        return False
