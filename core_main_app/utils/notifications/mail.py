import tasks.task_mail as task
import os
from django.utils.importlib import import_module

settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
USE_BACKGROUND_TASK = settings.USE_BACKGROUND_TASK
SERVER_EMAIL = settings.SERVER_EMAIL


def send_mail(recipient_list, subject, path_to_template, context={}, fail_silently=True, sender=SERVER_EMAIL):
    if USE_BACKGROUND_TASK:
        # Async call. Use celery
        task.send_mail.apply_async((recipient_list, subject, path_to_template, context, fail_silently, sender), countdown=1)
    else:
        # Sync call
        task.send_mail(recipient_list, subject, path_to_template, context, fail_silently, sender)


def send_mail_to_administrators(subject, path_to_template, context={}, fail_silently=True):
    if USE_BACKGROUND_TASK:
        # Async call. Use celery
        task.send_mail_to_administrators.apply_async((subject, path_to_template, context, fail_silently), countdown=1)
    else:
        # Sync call
        task.send_mail_to_administrators(subject, path_to_template, context, fail_silently)


def send_mail_to_managers(subject, path_to_template, context={}, fail_silently=True):
    if USE_BACKGROUND_TASK:
        # Async call. Use celery
        task.send_mail_to_managers.apply_async((subject, path_to_template, context, fail_silently), countdown=1)
    else:
        # Sync call
        task.send_mail_to_managers(subject, path_to_template, context, fail_silently)

