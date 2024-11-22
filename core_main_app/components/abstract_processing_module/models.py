""" Abstract model for processing modules
"""

import importlib

from django.db import models


class AbstractProcessingModule(models.Model):
    """Class to manage different types of processing modules"""

    RUN_ON_DEMAND = "DEMAND"
    RUN_ON_CREATE = "CREATE"
    RUN_ON_READ = "READ"
    RUN_ON_UPDATE = "UPDATE"
    RUN_ON_DELETE = "DELETE"
    RUN_STRATEGY = [
        (RUN_ON_DEMAND, "Run on demand"),
        (RUN_ON_CREATE, "Run on create"),
        (RUN_ON_READ, "Run on read"),
        (RUN_ON_UPDATE, "Run on update"),
        (RUN_ON_DELETE, "Run on delete"),
    ]

    name = models.CharField(
        max_length=256, blank=False, default=None, unique=True
    )
    run_strategy = models.CharField(
        max_length=20,
        choices=RUN_STRATEGY,
        default=RUN_ON_DEMAND,
    )

    parameters = models.JSONField(null=True, blank=True, default=None)
    processing_class = models.CharField(
        max_length=256, blank=False, null=False
    )

    class Meta:
        """Metadata information about processing module objects"""

        abstract = True

    def get_class(self):
        """Retrieve and instantiate the processing module class"""
        classpath = self.processing_class.split(".")
        module = importlib.import_module(".".join(classpath[:-1]))

        return getattr(module, classpath[-1])()

    def __str__(self):
        """Display the name of the blob module"""
        return self.name
