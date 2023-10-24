"""
    Common ajax
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from core_main_app.commons import exceptions
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.views.admin.forms import EditTemplateForm


class AddObjectModalView(CreateView):
    """Common AddObjectModalView.
    Should be used with add.html and add.js.
    """

    template_name = "core_main_app/common/commons/form.html"
    form_class = None
    model = None
    success_url = None
    success_message = None

    def form_invalid(self, form):
        """form_invalid

        Args:
            form:

        Return:
        """
        # Get initial response
        response = super().form_invalid(form)
        data = {"is_valid": False, "responseText": response.rendered_content}
        return JsonResponse(data)

    def form_valid(self, form):
        """form_valid

        Args:
            form:

        Return:
        """
        # This method is called when valid form data has been POSTed.
        # Call private save method
        # Populate self.object without committing to the database
        self.object = form.save(commit=False)
        self._save(form)
        if not form.is_valid():
            return self.form_invalid(form)

        data = {
            "is_valid": True,
            "url": self.get_success_url(),
        }

        if self.success_message:
            messages.success(self.request, self.success_message)

        return JsonResponse(data)

    def _save(self, form):
        # Save treatment.
        super().form_valid(form)

    @staticmethod
    def get_modal_html_path():
        """get_modal_html_path

        Args:

        Return:
        """
        return "core_main_app/common/modals/add_page_modal.html"

    @staticmethod
    def get_modal_js_path():
        """get_modal_js_path

        Args:

        Return:
        """
        return {
            "path": "core_main_app/common/js/modals/add.js",
            "is_raw": False,
        }


class EditObjectModalView(UpdateView):
    """Common EditObjectModalView.
    Should be used with edit_page_modal.html and edit.js.
    """

    template_name = "core_main_app/common/commons/form.html"
    form_class = None
    model = None
    success_url = None
    success_message = None

    def form_invalid(self, form):
        """form_invalid

        Args:
            form:

        Return:
        """
        # Get initial response
        response = super().form_invalid(form)
        data = {"is_valid": False, "responseText": response.rendered_content}
        return JsonResponse(data)

    def form_valid(self, form):
        """form_valid

        Args:
            form:

        Return:
        """
        # This method is called when valid form data has been POSTed.
        # Call private save method
        self._save(form)
        if form.is_valid():
            data = {
                "is_valid": True,
                "url": self.get_success_url(),
            }

            if self.success_message:
                messages.success(self.request, self.success_message)

            return JsonResponse(data)
        else:
            return self.form_invalid(form)

    def _save(self, form):
        # Save treatment.
        super().form_valid(form)

    @staticmethod
    def get_modal_html_path():
        """get_modal_html_path

        Args:

        Return:
        """
        return "core_main_app/common/modals/edit_page_modal.html"

    @staticmethod
    def get_modal_js_path():
        """get_modal_js_path

        Args:

        Return:
        """
        return {
            "path": "core_main_app/common/js/modals/edit.js",
            "is_raw": False,
        }


class DeleteObjectModalView(DeleteView):
    """Common DeleteObjectModalView.
    Should be used with delete_page_modal.html and delete.js.
    """

    template_name = "core_main_app/common/commons/form_delete.html"
    model = None
    field_for_name = None
    success_url = None
    success_message = None

    def form_valid(self, form):
        """Method is called when valid form data has been POSTed.

        Args:
            form:

        Return:
        """
        # Populate self.object without committing to the database and call _delete
        # method.
        try:
            self.object = self.get_object()
            self._delete(form)

            if self.success_message:
                messages.success(self.request, self.success_message)
        except Exception as exception:
            messages.error(self.request, str(exception))

        return JsonResponse({"url": self.get_success_url()})

    def _delete(self, form):
        """
        Delete treatment.
        """
        # Delete treatment.
        super().form_valid(form)

    def _get_object_name(self):
        """
        Get object name

        Returns:
        """
        object_name = ""
        if self.object:
            if self.field_for_name:
                object_name = getattr(
                    self.object, self.field_for_name, str(self.object)
                )
            else:
                object_name = str(self.object)

        return object_name

    def get_context_data(self, **kwargs):
        """get_context_data

        Args:

        Return:
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the object representation
        context["object_name"] = self._get_object_name()

        return context

    @staticmethod
    def get_modal_html_path():
        """get_modal_html_path

        Args:

        Return:
        """
        return "core_main_app/common/modals/delete_page_modal.html"

    @staticmethod
    def get_modal_js_path():
        """get_modal_js_path

        Args:

        Return:
        """
        return {
            "path": "core_main_app/common/js/modals/delete.js",
            "is_raw": False,
        }


@method_decorator(login_required, name="dispatch")
class EditTemplateVersionManagerView(EditObjectModalView):
    form_class = EditTemplateForm
    model = TemplateVersionManager
    success_url = reverse_lazy("core-admin:core_main_app_templates")
    success_message = "Name edited with success."

    def _save(self, form):
        # Save treatment.
        try:
            template_version_manager_api.edit_title(
                self.object,
                form.cleaned_data.get("title"),
                request=self.request,
            )
        except exceptions.NotUniqueError:
            form.add_error(
                None,
                "An object with the same name already exists. Please choose "
                "another name.",
            )
        except Exception as exception:
            form.add_error(None, str(exception))
