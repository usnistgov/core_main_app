""" User Preferences model
"""

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from pytz import common_timezones as pytz_common_timezones

from core_main_app.commons import exceptions


def validate_timezone(timezone):
    """
    validate_timezone
    """
    if timezone not in pytz_common_timezones:
        raise ValidationError("Invalid timezone value.")


class UserPreferences(models.Model):
    """User Preferences"""

    user_id = models.CharField(
        blank=False, max_length=200, null=False, unique=True
    )

    timezone = models.CharField(
        blank=True, null=True, max_length=200, validators=[validate_timezone]
    )

    class Meta:
        verbose_name = " User Preferences"
        verbose_name_plural = " User Preferences"

    @staticmethod
    def get_by_user(user):
        """Get user preferences relative to the given id

        Args:
            user:

        Returns:

        """
        try:
            return UserPreferences.objects.get(user_id=str(user.id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    def save_object(self):
        """Custom save

        Returns:

        """
        self.full_clean()
        return self.save()
