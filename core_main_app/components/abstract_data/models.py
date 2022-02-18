""" Abstract Data model
"""
from io import BytesIO

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.settings import (
    GRIDFS_DATA_COLLECTION,
    SEARCHABLE_DATA_OCCURRENCES_LIMIT,
    XML_POST_PROCESSOR,
    XML_FORCE_LIST,
)
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.datetime_tools.utils import datetime_now
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces


class AbstractData(Document):
    """AbstractData object"""

    dict_content = fields.DictField(blank=True)
    title = fields.StringField(blank=False, validation=not_empty_or_whitespaces)
    xml_file = fields.FileField(blank=False, collection_name=GRIDFS_DATA_COLLECTION)
    creation_date = fields.DateTimeField(blank=True, default=None)
    last_modification_date = fields.DateTimeField(blank=True, default=None)
    last_change_date = fields.DateTimeField(blank=True, default=None)

    _xml_content = None

    meta = {
        "abstract": True,
    }

    @property
    def xml_content(self):
        """Get xml content - read from a saved file.

        Returns:

        """
        # private field xml_content not set yet, and reference to xml_file to read is set
        if self._xml_content is None and self.xml_file is not None:
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

    def convert_and_save(self):
        """Save Data object and convert the xml to dict if needed.

        Returns:

        """
        self.convert_to_dict()
        self.convert_to_file()

        return self.save_object()

    def convert_to_dict(self):
        """Convert the xml contained in xml_content into a dictionary.

        Returns:

        """
        # transform xml content into a dictionary
        dict_content = xml_utils.raw_xml_to_dict(
            self.xml_content,
            postprocessor=XML_POST_PROCESSOR,
            force_list=XML_FORCE_LIST,
        )
        # if limit on element occurrences is set
        if SEARCHABLE_DATA_OCCURRENCES_LIMIT is not None:
            # Remove lists which size exceed the limit size
            xml_utils.remove_lists_from_xml_dict(
                dict_content, SEARCHABLE_DATA_OCCURRENCES_LIMIT
            )
        # store dictionary
        self.dict_content = dict_content

    def convert_to_file(self):
        """Convert the xml string into a file.

        Returns:

        """
        try:
            xml_file = BytesIO(self.xml_content.encode("utf-8"))
        except Exception:
            xml_file = BytesIO(self.xml_content)

        if self.xml_file.grid_id is None:
            # new file
            self.xml_file.put(xml_file, content_type="application/xml")
        else:
            # editing (self.xml_file gets a new id)
            self.xml_file.replace(xml_file, content_type="application/xml")

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
            return self.save()
        except mongoengine_errors.NotUniqueError as e:
            raise exceptions.NotUniqueError(e)
        except Exception as ex:
            raise exceptions.ModelError(ex)
