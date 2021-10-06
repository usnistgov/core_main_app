"""
Version Manager model
"""
from abc import abstractmethod

from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


# TODO: could make is_disabled a Status with other possible values taken from an enum


class Version(models.Model):
    """"""

    is_current = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)

    class Meta:
        abstract = True


class VersionManager(models.Model):
    """Version Manager"""

    title = models.CharField(
        unique=True,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
    )
    user = models.CharField(blank=True, max_length=200, null=True, default=None)
    is_disabled = models.BooleanField(default=False)
    # TODO: for now, set _cls for backward compatibility in apis
    _cls = models.CharField(default="VersionManager", max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def version_set(self):
        raise NotImplementedError("Implement in the child class.")

    @property
    @abstractmethod
    def class_name(self):
        raise NotImplementedError("Implement in the child class.")

    @property
    def current_version(self):
        return self.version_set.get(is_current=True)

    @property
    def disabled_version_set(self):
        return self.version_set.filter(is_disabled=True)

    # backward compatibility
    @property
    def versions(self):
        return [str(version.id) for version in self.version_set]

    # backward compatibility
    @property
    def current(self):
        return str(self.current_version.id)

    # backward compatibility
    @property
    def disabled_versions(self):
        return [str(version.id) for version in self.disabled_version_set]

    def save_version_manager(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        try:
            self._cls = self.class_name
            self.save()
        except IntegrityError as e:
            raise exceptions.NotUniqueError(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def clean(self):
        """Clean is called before saving

        Returns:

        """
        self.title = self.title.strip()
