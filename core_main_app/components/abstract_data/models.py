""" Abstract Data model
"""
from io import BytesIO

from core_main_app.settings import GRIDFS_DATA_COLLECTION, SEARCHABLE_DATA_OCCURRENCES_LIMIT
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces
from django_mongoengine import fields, Document


class AbstractData(Document):
    """ AbstractData object
    """
    dict_content = fields.DictField(blank=True)
    title = fields.StringField(blank=False, validation=not_empty_or_whitespaces)
    last_modification_date = fields.DateTimeField(blank=True, default=None)
    xml_file = fields.FileField(blank=False, collection_name=GRIDFS_DATA_COLLECTION)

    _xml_content = None

    meta = {
        'abstract': True,
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
                self._xml_content = xml_content.decode('utf-8') if xml_content else xml_content
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
        self._xml_content = value

    def convert_and_save(self):
        """ Save Data object and convert the xml to dict if needed.

        Returns:

        """
        self.convert_to_dict()
        self.convert_to_file()

        return self.save()

    def convert_to_dict(self):
        """ Convert the xml contained in xml_content into a dictionary.

        Returns:

        """
        # transform xml content into a dictionary
        dict_content = xml_utils.raw_xml_to_dict(self.xml_content, xml_utils.post_processor)
        # if limit on element occurrences is set
        if SEARCHABLE_DATA_OCCURRENCES_LIMIT is not None:
            # Remove lists which size exceed the limit size
            xml_utils.remove_lists_from_xml_dict(dict_content,
                                                 SEARCHABLE_DATA_OCCURRENCES_LIMIT)
        # store dictionary
        self.dict_content = dict_content

    def convert_to_file(self):
        """ Convert the xml string into a file.

        Returns:

        """
        try:
            xml_file = BytesIO(self.xml_content.encode('utf-8'))
        except Exception:
            xml_file = BytesIO(self.xml_content)

        if self.xml_file.grid_id is None:
            # new file
            self.xml_file.put(xml_file, content_type="application/xml")
        else:
            # editing (self.xml_file gets a new id)
            self.xml_file.replace(xml_file, content_type="application/xml")
