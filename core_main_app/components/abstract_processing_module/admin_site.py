""" Custom admin site for the Abstract Processing Module model
"""

from django.contrib import admin

from core_main_app.components.abstract_processing_module.forms import (
    AbstractProcessingModuleForm,
)


class AbstractProcessingModuleAdmin(admin.ModelAdmin):
    """Admin model for `AbstractProcessingModule` objects"""

    form = AbstractProcessingModuleForm
