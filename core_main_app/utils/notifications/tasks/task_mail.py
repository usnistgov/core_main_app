"""Mailing task
"""

from logging import getLogger

from celery import shared_task
from django.core.mail import (
    send_mail as django_send_mail,
    mail_admins,
    mail_managers,
    EmailMultiAlternatives,
)
from django.template import loader

from core_main_app.settings import (
    SERVER_EMAIL,
    EMAIL_SUBJECT_PREFIX,
    WEBSITE_CONTACTS,
)

logger = getLogger(__name__)


@shared_task
def send_mail(
    recipient_list,
    subject,
    body,
    fail_silently=True,
    sender=SERVER_EMAIL,
):
    """Send email.

    Args:
        recipient_list:
        subject:
        body:
        fail_silently:
        sender:

    Returns:

    """
    try:

        # Send mail
        django_send_mail(
            subject=EMAIL_SUBJECT_PREFIX + subject,
            message="",
            from_email=sender,
            recipient_list=recipient_list,
            html_message=body,
            fail_silently=fail_silently,
        )
    except Exception as exception:
        raise exception


@shared_task
def send_mail_to_administrators(
    subject, path_to_template, context=None, fail_silently=True
):
    """Send email to administrators.

    Args:
        subject:
        path_to_template:
        context:
        fail_silently:

    Returns:

    """
    if context is None:
        context = {}
    try:
        # Render the given template with context information
        template = loader.get_template(path_to_template)
        message = template.render(context)
        # Send mail
        mail_admins(
            subject=subject,
            message="",
            html_message=message,
            fail_silently=fail_silently,
        )
    except Exception as exception:
        logger.warning(
            "send_mail_to_administrators threw an exception:  %s",
            str(exception),
        )


@shared_task
def send_mail_to_managers(
    subject, path_to_template, context=None, fail_silently=True
):
    """Send email to managers.

    Args:
        subject:
        path_to_template:
        context:
        fail_silently:

    Returns:

    """
    if context is None:
        context = {}
    try:
        # Render the given template with context information
        template = loader.get_template(path_to_template)
        message = template.render(context)
        # Send mail
        mail_managers(
            subject=subject,
            message="",
            html_message=message,
            fail_silently=fail_silently,
        )
    except Exception as exception:
        logger.warning(
            "send_mail_to_managers throws an exception: %s", str(exception)
        )


@shared_task
def send_mail_to_website_contacts(
    subject, path_to_template, context=None, fail_silently=True
):
    """Send a message to the admins contacts, as defined by the WEBSITE_CONTACTS setting.
    From: https://github.com/django/django/blob/main/django/core/mail/__init__.py
    """
    if not WEBSITE_CONTACTS:
        return
    if not all(
        isinstance(a, (list, tuple)) and len(a) == 2 for a in WEBSITE_CONTACTS
    ):
        raise ValueError(
            "The WEBSITE_CONTACTS setting must be a list of 2-tuples."
        )

    if context is None:
        context = {}
    try:
        # Render the given template with context information
        template = loader.get_template(path_to_template)
        message = template.render(context)

        mail = EmailMultiAlternatives(
            "%s%s" % (EMAIL_SUBJECT_PREFIX, subject),
            message,
            SERVER_EMAIL,
            [a[1] for a in WEBSITE_CONTACTS],
        )
        mail.send(fail_silently=fail_silently)
    except Exception as exception:
        logger.warning(
            "send_mail_to_managers throws an exception: %s", str(exception)
        )
