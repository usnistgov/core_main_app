""" Abstract Data model
"""
from django.contrib.postgres.search import SearchVectorField
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.settings import (
    SEARCHABLE_DATA_OCCURRENCES_LIMIT,
)
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.datetime_tools.utils import datetime_now


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
    xml_file = models.TextField(blank=False)
    vector_column = SearchVectorField(null=True)
    creation_date = models.DateTimeField(blank=True, default=None, null=True)
    last_modification_date = models.DateTimeField(blank=True, default=None, null=True)
    last_change_date = models.DateTimeField(blank=True, default=None, null=True)

    class Meta:
        abstract = True

    @property
    def xml_content(self):
        """Get xml content - read from a saved file.

        Returns:

        """
        return self.xml_file

    @xml_content.setter
    def xml_content(self, value):
        """Set xml content - to be saved as a file.

        Args:
            value:

        Returns:

        """
        # update modification times
        self.last_modification_date = datetime_now()
        # update content
        self.xml_file = value

    def convert_and_save(self):
        """Save Data object and convert the xml to dict if needed.

        Returns:

        """
        self.convert_to_dict()
        self.convert_to_file()

        self.save_object()

    def convert_to_dict(self):
        """Convert the xml contained in xml_content into a dictionary.

        Returns:

        """
        # TODO: avoid duplicating dict_content if mongo indexing?
        # transform xml content into a dictionary
        self.dict_content = xml_utils.raw_xml_to_dict(
            self.xml_content,
            xml_utils.post_processor,
            list_limit=SEARCHABLE_DATA_OCCURRENCES_LIMIT,
        )

    def convert_to_file(self):
        """Convert the xml string into a file.

        Returns:

        """
        self.xml_file = self.xml_content

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
            self.save()
        except IntegrityError as e:
            raise exceptions.NotUniqueError(e)
        except Exception as ex:
            raise exceptions.ModelError(ex)
