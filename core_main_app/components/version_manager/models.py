"""
Version Manager model
"""
from abc import abstractmethod

from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces


# TODO: could make is_disabled a Status with other possible values taken from an enum


class Version(models.Model):
    """Version"""

    is_current = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)

    class Meta:
        """Meta"""

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
        """Meta"""

        abstract = True

    @property
    @abstractmethod
    def version_set(self):
        """version_set

        Returns:

        """
        raise NotImplementedError("Implement in the child class.")

    @property
    @abstractmethod
    def class_name(self):
        """class_name

        Returns:

        """
        raise NotImplementedError("Implement in the child class.")

    @property
    def current_version(self):
        """current_version"""
        return self.version_set.get(is_current=True)

    @property
    def disabled_version_set(self):
        """disabled_version_set"""
        return self.version_set.filter(is_disabled=True)

    @property
    def versions(self):
        """versions (backward compatibility)"""
        return [str(version.id) for version in self.version_set]

    @property
    def current(self):
        """current (backward compatibility)"""
        return str(self.current_version.id)

    @property
    def disabled_versions(self):
        """disabled_versions (backward compatibility)"""
        return [str(version.id) for version in self.disabled_version_set]

    def save_version_manager(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        try:
            self._cls = self.class_name
            self.clean()
            self.save()
        except IntegrityError as exception:
            raise exceptions.NotUniqueError(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def clean(self):
        """Clean is called before saving

        Returns:

        """
        not_empty_or_whitespaces(self.title)
        self.title = self.title.strip()

    def __str__(self):
        """Version Manager as string

        Returns:

        """
        return self.title
