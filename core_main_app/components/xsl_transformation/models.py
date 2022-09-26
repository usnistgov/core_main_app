""" XslTransformation model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.settings import XSLT_UPLOAD_DIR, CHECKSUM_ALGORITHM
from core_main_app.utils.checksum import compute_checksum
from core_main_app.utils.storage.storage import core_file_storage


class XslTransformation(models.Model):
    """XslTransformation object"""

    name = models.CharField(
        unique=True,
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
    filename = models.CharField(
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
        upload_to=XSLT_UPLOAD_DIR,
        storage=core_file_storage(model="xsl_transformation"),
    )
    checksum = models.CharField(
        max_length=512, blank=True, default=None, null=True
    )
    _content = None

    @property
    def content(self):
        """Read XSLT content

        Returns:

        """
        if not self._content:
            self._content = self.file.read().decode("utf-8")
        return self._content

    @content.setter
    def content(self, xsd_content):
        """Set xslt content

        Args:
            xsd_content:

        Returns:

        """
        # Set template content
        self._content = xsd_content

    def __str__(self):
        """String representation of an object.

        Returns:
            String representation

        """
        return self.name

    @staticmethod
    def get_all():
        """Get all XSL Transformations.

        Returns:

        """
        return XslTransformation.objects.all()

    @staticmethod
    def get_by_id_list(list_id):
        """Return the object with the given list id.

        Args:
            list_id:

        Returns:
            Object collection
        """
        return XslTransformation.objects.filter(pk__in=list_id)

    @staticmethod
    def get_by_name(xslt_name):
        """Get XSL Transformation by name.

        Args:
            xslt_name:

        Returns:

        """
        try:
            return XslTransformation.objects.get(name=xslt_name)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_id(xslt_id):
        """Get an XSLT document by its id.

        Args:
            xslt_id: Id.

        Returns:
            XslTransformation object.

        """
        try:
            return XslTransformation.objects.get(pk=xslt_id)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def save_object(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        try:
            if self._content:
                self.file = SimpleUploadedFile(
                    name=self.filename,
                    content=self._content.encode("utf-8"),
                    content_type="application/xml",
                )
            if self.content and CHECKSUM_ALGORITHM:
                self.checksum = compute_checksum(
                    self.content.encode(), CHECKSUM_ALGORITHM
                )
            self.clean()
            return self.save()
        except IntegrityError as exception:
            raise exceptions.NotUniqueError(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def clean(self):
        """Clean is called before saving

        Returns:

        """
        self.name = self.name.strip()
        self.filename = self.filename.strip()
