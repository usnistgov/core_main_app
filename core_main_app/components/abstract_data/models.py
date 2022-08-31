""" Abstract Data model
"""

from django.contrib.postgres.search import SearchVectorField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.settings import (
    SEARCHABLE_DATA_OCCURRENCES_LIMIT,
    MONGODB_INDEXING,
    XML_POST_PROCESSOR,
    XML_FORCE_LIST,
    CHECKSUM_ALGORITHM,
)
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.checksum import compute_checksum
from core_main_app.utils.datetime_tools.utils import datetime_now
from core_main_app.utils.storage.storage import core_file_storage, user_directory_path


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
    xml_file = models.FileField(
        blank=False,
        max_length=250,
        upload_to=user_directory_path,
        storage=core_file_storage(model="data"),
    )
    checksum = models.CharField(max_length=512, blank=True, default=None, null=True)
    vector_column = SearchVectorField(null=True)
    creation_date = models.DateTimeField(blank=True, default=None, null=True)
    last_modification_date = models.DateTimeField(blank=True, default=None, null=True)
    last_change_date = models.DateTimeField(blank=True, default=None, null=True)
    _xml_content = None

    class Meta:
        """Meta"""

        abstract = True

    @property
    def xml_content(self):
        """Get xml content - read from a saved file.

        Returns:

        """
        # private field xml_content not set yet, and reference to xml_file to read is set
        if self._xml_content is None and self.xml_file.name:
            # read xml file into xml_content field
            xml_content = self.xml_file.read()
            try:
                self._xml_content = (
                    xml_content.decode("utf-8") if xml_content else xml_content
                )
            except AttributeError:
                self._xml_content = xml_content
        # return xml content
        return self._xml_content

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
        self._xml_content = value

    def get_dict_content(self):
        """Get dict_content from object or from MongoDB

        Returns:

        """
        raise NotImplementedError("get_dict_content is not implemented")

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
        # if data stored in mongo, don't store dict_content
        if MONGODB_INDEXING:
            return
        # transform xml content into a dictionary
        self.dict_content = xml_utils.raw_xml_to_dict(
            self.xml_content,
            postprocessor=XML_POST_PROCESSOR,
            force_list=XML_FORCE_LIST,
            list_limit=SEARCHABLE_DATA_OCCURRENCES_LIMIT,
        )

    def convert_to_file(self):
        """Convert the xml string into a file.

        Returns:

        """
        try:
            xml_content = self.xml_content.encode("utf-8")
        except UnicodeEncodeError:
            xml_content = self.xml_content

        self.xml_file = SimpleUploadedFile(
            name=self.title, content=xml_content, content_type="application/xml"
        )

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
            if self.xml_content and CHECKSUM_ALGORITHM:
                self.checksum = compute_checksum(
                    self.xml_content.encode(), CHECKSUM_ALGORITHM
                )
            self.save()
        except IntegrityError as exception:
            raise exceptions.NotUniqueError(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
