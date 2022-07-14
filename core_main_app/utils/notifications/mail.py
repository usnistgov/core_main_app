"""Mailing util
"""
from django.template import loader

from core_main_app.settings import SERVER_EMAIL, SEND_EMAIL_ASYNC
from core_main_app.templatetags.stripjs import stripjs
from core_main_app.utils.notifications.tasks import task_mail as task


def send_mail_from_template(
    recipient_list,
    subject,
    path_to_template,
    context=None,
    fail_silently=True,
    sender=SERVER_EMAIL,
):
    """Send email.

    Args:
        recipient_list:
        subject:
        path_to_template:
        context:
        fail_silently:
        sender:

    Returns:

    """
    # Render the given template with context information
    if context is None:
        context = {}
    template = loader.get_template(path_to_template)
    body = template.render(context)
    _send_email(
        recipient_list=recipient_list,
        subject=subject,
        body=body,
        fail_silently=fail_silently,
        sender=sender,
    )


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

    stripped_body = stripjs(body)
    _send_email(
        recipient_list=recipient_list,
        subject=subject,
        body=stripped_body,
        fail_silently=fail_silently,
        sender=sender,
    )


def _send_email(recipient_list, subject, body, fail_silently, sender):
    """Send email async or sync from the rendered template

    Args:
        recipient_list:
        subject:
        body:
        fail_silently:
        sender:

    Returns:

    """
    if SEND_EMAIL_ASYNC:
        # Async call. Use celery
        task.send_mail.apply_async(
            (
                recipient_list,
                subject,
                body,
                fail_silently,
                sender,
            ),
            countdown=1,
        )
    else:
        # Sync call
        task.send_mail(
            recipient_list=recipient_list,
            subject=subject,
            body=body,
            fail_silently=fail_silently,
            sender=sender,
        )


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
    if SEND_EMAIL_ASYNC:
        # Async call. Use celery
        task.send_mail_to_administrators.apply_async(
            (subject, path_to_template, context, fail_silently), countdown=1
        )
    else:
        # Sync call
        task.send_mail_to_administrators(
            subject, path_to_template, context, fail_silently
        )


def send_mail_to_managers(subject, path_to_template, context=None, fail_silently=True):
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
    if SEND_EMAIL_ASYNC:
        # Async call. Use celery
        task.send_mail_to_managers.apply_async(
            (subject, path_to_template, context, fail_silently), countdown=1
        )
    else:
        # Sync call
        task.send_mail_to_managers(subject, path_to_template, context, fail_silently)
