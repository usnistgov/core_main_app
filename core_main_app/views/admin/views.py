from django.http.response import HttpResponseRedirect
from django.template import loader
from django.template.context import Context
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import escape as html_escape
from django.core.urlresolvers import reverse

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.utils.rendering import render
from core_main_app.utils.xml import get_imports_and_includes
from core_main_app.views.admin.forms import UploadTemplateForm


@staff_member_required
def manage_templates(request):
    """
    Page that allows to upload new schemas and manage the existing ones
    :param request:
    :return:
    """
    # get all current templates
    current_templates = template_version_manager_api.get_global_version_managers()

    context = {
        'objects': current_templates,
        'js': ['core_main_app/admin/js/template_manager.js', 'core_main_app/admin/js/template.js'],
    }
    return render(request,
                  'core_main_app/admin/template_manager.html',
                  context)


@staff_member_required
def upload_xsd(request):
    """
    Form that allows to upload new templates
    :param request:
    :return:
    """
    # method is POST
    if request.method == 'POST':

        form = UploadTemplateForm(request.POST,  request.FILES)

        if form.is_valid():
            # get the schema name
            name = request.POST['name']
            # get the file from the form
            xsd_file = request.FILES['xsd_file']
            # put the cursor at the beginning of the file
            xsd_file.seek(0)
            # read the content of the file
            xsd_data = xsd_file.read()

            try:
                template = Template(filename=xsd_file.name, content=xsd_data)
                template_version_manager = TemplateVersionManager(title=name)
                template_version_manager_api.insert(template_version_manager, template)
                # XML schema loaded with success
                messages.add_message(request, messages.INFO, 'Template uploaded with success.')
                return HttpResponseRedirect(reverse("admin:core_main_app_templates"))
            except exceptions.XSDError, e:
                imports, includes = get_imports_and_includes(xsd_data)
                # a problem with includes/imports has been detected
                if len(includes) > 0 or len(imports) > 0:
                    # build dependency resolver
                    dependency_resolver_html = _get_dependency_resolver_html(imports, includes, xsd_data, xsd_file.name)

                    context = {
                        'dependency_resolver': dependency_resolver_html,
                    }

                    return _upload_response(request, form, params=context)
                else:
                    return _upload_response(request, form, error_message=e.message)
            except Exception, e:
                return _upload_response(request, form, error_message=e.message)
        else:
            # Display error from the form
            return _upload_response(request, form)
    # method is GET
    else:
        # render the form to upload a template
        return _upload_response(request, UploadTemplateForm())


def _upload_response(request, form, params=None, error_message=""):
    """
    Return http response set with context and errors
    :param request:
    :param form:
    :param error_message:
    :return:
    """
    context = {
        'upload_form': form,
        'errors': error_message.replace('"', '\''),
        'js': ['core_main_app/admin/js/dependency_resolver.js',
               'core_main_app/admin/js/template.js'],
    }
    if params is not None:
        context.update(params)

    return render(request,
                  'core_main_app/admin/upload_xsd.html',
                  context)


def _get_dependency_resolver_html(imports, includes, xsd_data, filename):
    """
    Return HTML for dependency resolver form
    :param imports:
    :param includes:
    :param xsd_data:
    :return:
    """
    # build the list of dependencies
    current_templates = template_version_manager_api.get_global_version_managers()
    list_dependencies_template = loader.get_template('core_main_app/admin/list_dependencies.html')
    context = Context({
        'templates': current_templates,
    })
    list_dependencies_html = list_dependencies_template.render(context)

    # build the dependency resolver form
    dependency_resolver_template = loader.get_template('core_main_app/admin/dependency_resolver.html')
    context = Context({
        'imports': imports,
        'includes': includes,
        'xsd_content': html_escape(xsd_data),
        'filename': filename,
        'dependencies': list_dependencies_html,
    })
    return dependency_resolver_template.render(context)
