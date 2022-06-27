from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(subject, data, template, email):
    """
    This function sends an email.
    Args:
        subject (str): Is the subject of the email.
        data (dict): It is the data to pass to the email template.
        template (str): Is the path to the email tempate.
        email (str): Is the destination email.
    """
    html_msg = render_to_string(
        template,
        context=data
    )

    plain_message = strip_tags(html_msg)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email, ]

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_msg
    )
