""" Abstract Data model
"""
from abc import abstractmethod

from django.contrib.postgres.search import SearchVectorField
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.settings import (
    CHECKSUM_ALGORITHM,
)
from core_main_app.utils.checksum import compute_checksum
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.storage.storage import (
    core_file_storage,
    user_directory_path,
)


class AbstractData(models.Model):
    """AbstractData object"""

    dict_content = models.JSONField(blank=True, null=True)
    title = models.CharField(
        blank=False,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
    )
    file = models.FileField(
        blank=False,
        max_length=250,
        upload_to=user_directory_path,
        storage=core_file_storage(model="data"),
    )
    checksum = models.CharField(
        max_length=512, blank=True, default=None, null=True
    )
    vector_column = SearchVectorField(null=True)
    creation_date = models.DateTimeField(blank=True, default=None, null=True)
    last_modification_date = models.DateTimeField(
        blank=True, default=None, null=True
    )
    last_change_date = models.DateTimeField(
        blank=True, default=None, null=True
    )
    _content = None

    class Meta:
        """Meta"""

        abstract = True

    @property
    def content(self):
        """Get content - read from a saved file.

        Returns:

        """
        # private field content not set yet, and reference to file to read is set
        if self._content is None and self.file.name:
            # read xml file into content field
            file_content = self.file.read()
            try:
                self._content = (
                    file_content.decode("utf-8")
                    if file_content
                    else file_content
                )
            except AttributeError:
                self._content = file_content
        # return content
        return self._content

    @content.setter
    def content(self, value):
        """Set content - to be saved as a file.

        Args:
            value:

        Returns:

        """
        # update modification times
        self.last_modification_date = datetime_now()
        # update content
        self._content = value

    @property
    def xml_content(self):
        """Get content - backward compatibility"""
        return self.content

    @xml_content.setter
    def xml_content(self, value):
        """Set content - backward compatibility"""
        self.content = value

    def get_dict_content(self):
        """Get dict_content from object or from MongoDB

        Returns:

        """
        raise NotImplementedError("get_dict_content is not implemented")

    def convert_and_save(self):
        """Convert data object to file (storage) and dict (indexing), then save it.

        Returns:

        """
        self.convert_to_dict()
        self.convert_to_file()

        self.save_object()

    @abstractmethod
    def convert_to_dict(self):
        """Convert the data into a dictionary.

        Returns:

        """
        raise NotImplementedError("convert_to_dict is not implemented.")

    @abstractmethod
    def convert_to_file(self):
        """Convert the data into a file.

        Returns:

        """
        raise NotImplementedError("convert_to_file is not implemented.")

    def save_object(self):
        """Custom save. Set the datetime fields and save.

        Returns:

        """
        try:
            # initialize times
            now = datetime_now()
            # update change date every time the data is updated
            self.last_change_date = now
            if not self.id:
                # initialize when first created
                self.creation_date = now
                # initialize when first saved, then only updates when content is updated
                self.last_modification_date = now
            if self.content and CHECKSUM_ALGORITHM:
                self.checksum = compute_checksum(
                    str(self.content).encode(), CHECKSUM_ALGORITHM
                )
            self.save()
        except IntegrityError as exception:
            raise exceptions.NotUniqueError(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
