"""Mailing util
"""
import core_main_app.utils.notifications.tasks.task_mail as task
from core_main_app.settings import SERVER_EMAIL, USE_BACKGROUND_TASK


def send_mail(recipient_list, subject, path_to_template, context={}, fail_silently=True, sender=SERVER_EMAIL):
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
    if USE_BACKGROUND_TASK:
        # Async call. Use celery
        task.send_mail.apply_async((recipient_list, subject, path_to_template, context, fail_silently, sender), countdown=1)
    else:
        # Sync call
        task.send_mail(recipient_list, subject, path_to_template, context, fail_silently, sender)


def send_mail_to_administrators(subject, path_to_template, context={}, fail_silently=True):
    """Send email to administrators.

    Args:
        subject:
        path_to_template:
        context:
        fail_silently:

    Returns:

    """
    if USE_BACKGROUND_TASK:
        # Async call. Use celery
        task.send_mail_to_administrators.apply_async((subject, path_to_template, context, fail_silently), countdown=1)
    else:
        # Sync call
        task.send_mail_to_administrators(subject, path_to_template, context, fail_silently)


def send_mail_to_managers(subject, path_to_template, context={}, fail_silently=True):
    """Send email to managers.

    Args:
        subject:
        path_to_template:
        context:
        fail_silently:

    Returns:

    """
    if USE_BACKGROUND_TASK:
        # Async call. Use celery
        task.send_mail_to_managers.apply_async((subject, path_to_template, context, fail_silently), countdown=1)
    else:
        # Sync call
        task.send_mail_to_managers(subject, path_to_template, context, fail_silently)

