from django.conf import settings

# SECRET_KEY = getattr(settings, 'SECRET_KEY', 'ponq)(gd8hm57799)$lup4g9kyvp0l(9)k-3!em7dddn^(y)!5')

SECRET_KEY = 'ponq)(gd8hm57799)$lup4g9kyvp0l(9)k-3!em7dddn^(y)!5'

# Celery configuration
USE_BACKGROUND_TASK = getattr(settings, 'USE_BACKGROUND_TASK', False)
BROKER_URL = getattr(settings, 'BROKER_URL', 'redis://localhost:6379/0')
BROKER_TRANSPORT_OPTIONS = getattr(settings, 'BROKER_TRANSPORT_OPTIONS', {'visibility_timeout': 3600})
CELERY_RESULT_BACKEND = getattr(settings, 'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
BROKER_TRANSPORT_OPTIONS = getattr(settings, 'BROKER_TRANSPORT_OPTIONS', {'fanout_prefix': True,
                                                                          'fanout_patterns': True})

# SMTP Configuration
USE_EMAIL = getattr(settings, 'USE_EMAIL', False)
SERVER_EMAIL = getattr(settings, 'SERVER_EMAIL', 'noreply@curator.org')
ADMINS = getattr(settings, 'ADMINS', [('admin', 'admin@curator.org')])
MANAGERS = getattr(settings, 'MANAGERS', [('manager', 'moderator@curator.org')])
EMAIL_SUBJECT_PREFIX = getattr(settings, 'EMAIL_SUBJECT_PREFIX', "[CURATOR] ")


INSTALLED_APPS = (
    'core_main_app',
)
