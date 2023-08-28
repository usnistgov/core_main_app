"""
Template models
"""
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import RegexValidator
from django.db import models, IntegrityError
from django.db.models import Q

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.version_manager.models import Version
from core_main_app.settings import XSD_UPLOAD_DIR, CHECKSUM_ALGORITHM
from core_main_app.utils.checksum import compute_checksum
from core_main_app.utils.file import (
    get_template_file_content_type_for_template_format,
)
from core_main_app.utils.storage.storage import core_file_storage
from core_main_app.utils.validation.regex_validation import (
    not_empty_or_whitespaces,
)


class Template(Version):
    """Represents an XML schema template that defines the structure of data"""

    class_name = "Template"

    XSD = "XSD"
    JSON = "JSON"
    FORMAT_CHOICES = [
        (XSD, "XML Schema"),
        (JSON, "JSON Schema"),
    ]
    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        default=XSD,
    )

    version_manager = models.ForeignKey(
        TemplateVersionManager,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    filename = models.CharField(
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
        # NOTE: needed to check owner during upload (cf. core_main_app.utils.xml._get_schema_location_uri)
        upload_to=XSD_UPLOAD_DIR,
        storage=core_file_storage(model="template"),
    )
    user = models.CharField(
        blank=True, max_length=200, null=True, default=None
    )
    # NOTE: checksum is a hash of the file using a hash algorithm defined in CHECKSUM_ALGORITHM setting
    checksum = models.CharField(
        max_length=512, blank=True, default=None, null=True
    )
    # NOTE: _hash is a custom hash (XSD: removes white spaces, comments, and order elements before hashing)
    _hash = models.CharField(max_length=200)
    _display_name = models.CharField(blank=True, max_length=200)
    dependencies = models.ManyToManyField(
        "self", blank=True, default=[], symmetrical=False
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    _cls = models.CharField(default="Template", max_length=200)
    _content = None

    @property
    def content(self):
        """Read template content

        Returns:

        """
        if not self._content:
            self._content = self.file.read().decode("utf-8")
        return self._content

    @content.setter
    def content(self, xsd_content):
        """Set template content

        Args:
            xsd_content:

        Returns:

        """
        # Set template content
        self._content = xsd_content

    @property
    def hash(self):
        """Read template hash

        Returns:
            1) Check backward compatibility: continue returning custom XSD hash if set.
            2) Check optional setting: return a checksum for any file formats if set,
            3) Returns None if not set.

        """
        if self._hash:
            return self._hash
        elif self.checksum:
            return self.checksum
        return None

    @hash.setter
    def hash(self, hash_value):
        """Set template hash

        Args:
            hash_value:

        Returns:

        """
        # Set template hash
        self._hash = hash_value

    @staticmethod
    def get_all(is_cls, users=None):
        """Return all templates.

        Args:
            is_cls (bool): True if filtering by templates only.
            users (list|None): List of users having access to the template.

        Returns:
            list<Template> - List of template following the query parameters.
        """
        template_query = Q()

        if is_cls:  # will return all Template object only
            template_query &= Q(_cls=Template.class_name)

        if users is not None:  # select specific user if it is defined
            template_query &= users

        return Template.objects.filter(template_query).all()

    @staticmethod
    def get_by_id(template_id):
        """Return a template by its id.

        Args:
            template_id:

        Returns:

        """
        try:
            return Template.objects.get(pk=template_id)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all_by_hash(template_hash, users):
        """Return all template having the given hash.

        Args:
            template_hash: Template hash.
            users:

        Returns:
            List of Template instance.

        """
        if users is not None:
            return Template.objects.filter(
                Q(_hash=template_hash) & users
            ).all()
        return Template.objects.filter(_hash=template_hash).all()

    @staticmethod
    def get_all_by_hash_list(template_hash_list, users):
        """Return all template having the given hash list.

        Args:
            template_hash_list: Template hash list.
            users:

        Returns:
            List of Template instance.

        """
        if users is not None:
            return Template.objects.filter(
                Q(_hash__in=template_hash_list) & users
            ).all()
        return Template.objects.filter(_hash__in=template_hash_list).all()

    @staticmethod
    def get_all_by_id_list(template_id_list, users=None):
        """Return all template with id in list.

        Args:
            template_id_list:
            users:

        Returns:

        """
        if users is not None:
            return Template.objects.filter(
                Q(pk__in=template_id_list) & users
            ).all()
        return Template.objects.filter(pk__in=template_id_list).all()

    @property
    def display_name(self):
        """Return template name to display.

        Returns:

        """
        if self._display_name is not None:
            return self._display_name
        return self.filename

    @display_name.setter
    def display_name(self, value):
        """Set template name to display.

        Args:
            value:

        Returns:

        """
        self._display_name = value

    def save_template(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        try:
            self._cls = self.class_name
            if self._content:
                self.file = SimpleUploadedFile(
                    name=self.filename,
                    content=self._content.encode("utf-8"),
                    content_type=get_template_file_content_type_for_template_format(
                        self.format
                    ),
                )
            not_empty_or_whitespaces(self.filename)
            if self.content and CHECKSUM_ALGORITHM:
                self.checksum = compute_checksum(
                    self.content.encode(), CHECKSUM_ALGORITHM
                )
            self.save()
        except IntegrityError as exception:
            raise exceptions.NotUniqueError(str(exception))
        except ValidationError as exception:
            raise exception
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def __str__(self):
        """Template object as string

        Returns:

        """
        return self.display_name
