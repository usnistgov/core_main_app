""" Custom admin site for the Blob Module model
"""

import json

from django import forms
from django.contrib import admin

from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)


class RunStrategyListWidget(forms.widgets.Widget):
    """Widget to translate run strategy from JSONField to a proper HTML form."""

    def value_from_datadict(self, data, files, name):
        """Format the output value given form data.

        Args:
            data:
            files:
            name:

        Returns:
            Value to be saved for the field
        """
        return json.dumps(
            [
                item
                for item in data
                if item in AbstractProcessingModule.RUN_STRATEGY_MAP.keys()
            ]
        )

    def render(self, name, value, attrs=None, renderer=None):
        """Render the proper form given an output value.

        Args:
            name:
            value:
            attrs:
            renderer:

        Returns:
            HTML template to present the widget.
        """
        value_list = json.loads(value)
        html = []
        for (
            item_value,
            item_name,
        ) in AbstractProcessingModule.RUN_STRATEGY_MAP.items():
            html.append('<li style="display: flex">')
            html.append(
                '<input type="checkbox" name="%s" id="%s" value="on"%s>'
                % (
                    item_value,
                    item_value,
                    " checked" if item_value in value_list else "",
                )
            )
            html.append(
                '<label for="%s" style="margin: 0 0.25rem">%s</label>'
                % (item_value, item_name)
            )
            html.append("</li>")
        return '<ul style="margin: 0">' + "".join(html) + "</ul>"


class AbstractProcessingModuleForm(forms.ModelForm):
    """Model form for `AbstractProcessingModule` objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["run_strategy_list"].widget = RunStrategyListWidget()


class AbstractProcessingModuleAdmin(admin.ModelAdmin):
    """Admin model for `AbstractProcessingModule` objects"""

    form = AbstractProcessingModuleForm
