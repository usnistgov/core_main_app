from django.http.response import HttpResponseRedirect
from django.template import loader
from django.template.context import Context
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import escape as html_escape
from django.core.urlresolvers import reverse

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.rendering import render
from core_main_app.utils.xml import get_imports_and_includes
from core_main_app.views.admin.forms import UploadTemplateForm, UploadVersionForm


@staff_member_required
def manage_templates(request):
    """View that allows template management

    Args:
        request:

    Returns:

    """
    # get all current templates
    current_templates = template_version_manager_api.get_global_version_managers()

    context = {
        'objects': current_templates
    }

    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/template_manager.js',
                "raw": False
            },
            {
                "path": 'core_main_app/admin/js/template.js',
                "raw": False
            }
        ]
    }

    return render(request,
                  'core_main_app/admin/template_manager.html',
                  assets=assets,
                  context=context)


@staff_member_required
def manage_template_versions(request, version_manager_id):
    """View that allows template versions management

    Args:
        request:
        version_manager_id:

    Returns:

    """
    # get the version manager
    version_manager = None

    try:
        version_manager = version_manager_api.get(version_manager_id)
    except:
        # TODO: catch good exception, redirect to error page
        pass

    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/template_versions_manager.js',
                "raw": False
            },
            {
                "path": 'core_main_app/admin/js/template.js',
                "raw": False
            }
        ]
    }

    context = {
        'version_manager': version_manager,
    }

    return render(request,
                  'core_main_app/admin/template_versions_manager.html',
                  assets=assets,
                  context=context)


@staff_member_required
def upload_template(request):
    """Upload template

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/dependency_resolver.js',
                "raw": False
            },
            {
                "path": 'core_main_app/admin/js/template.js',
                "raw": False
            }
        ]
    }

    context = {
        'url': reverse("admin:core_main_app_upload_template"),
        'redirect_url': reverse("admin:core_main_app_templates")
    }

    # method is POST
    if request.method == 'POST':

        form = UploadTemplateForm(request.POST,  request.FILES)
        context['upload_form'] = form

        if form.is_valid():
            return _save_template(request, assets, context)
        else:
            # Display error from the form
            return _upload_template_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context['upload_form'] = UploadTemplateForm()
        return _upload_template_response(request, assets, context)


@staff_member_required
def upload_template_version(request, version_manager_id):
    """Upload template version

    Args:
        request:
        version_manager_id:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": 'core_main_app/admin/js/dependency_resolver.js',
                "raw": False
            },
            {
                "path": 'core_main_app/admin/js/template.js',
                "raw": False
            }
        ]
    }

    template_version_manager = version_manager_api.get(version_manager_id)
    context = {
        'version_manager': template_version_manager,
        'url': reverse("admin:core_main_app_upload_template_version",
                       kwargs={'version_manager_id': template_version_manager.id}),
        'redirect_url': reverse("admin:core_main_app_manage_template_versions",
                                kwargs={'version_manager_id': template_version_manager.id})
    }

    # method is POST
    if request.method == 'POST':
        form = UploadVersionForm(request.POST,  request.FILES)
        context['upload_form'] = form

        if form.is_valid():
            return _save_template_version(request, assets, context, template_version_manager)
        else:
            # Display errors from the form
            return _upload_template_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context['upload_form'] = UploadVersionForm()
        return _upload_template_response(request, assets, context)


def _save_template(request, assets, context):
    """Saves a template

    Args:
        request:
        context:

    Returns:

    """
    # get the schema name
    name = request.POST['name']
    # get the file from the form
    xsd_file = request.FILES['xsd_file']
    # read the content of the file
    xsd_data = _read_xsd_file(xsd_file)

    try:
        template = Template(filename=xsd_file.name, content=xsd_data)
        template_version_manager = TemplateVersionManager(title=name)
        template_version_manager_api.insert(template_version_manager, template)
        return HttpResponseRedirect(reverse("admin:core_main_app_templates"))
    except exceptions.XSDError, xsd_error:
        return _handle_xsd_errors(request, assets, context, xsd_error, xsd_data, xsd_file.name)
    except Exception, e:
        context['errors'] = html_escape(e.message)
        return _upload_template_response(request, assets, context)


def _save_template_version(request, assets, context, template_version_manager):
    """Saves a template version

    Args:
        request:
        context:
        template_version_manager:

    Returns:

    """
    # get the file from the form
    xsd_file = request.FILES['xsd_file']
    # read the content of the file
    xsd_data = _read_xsd_file(xsd_file)

    try:
        template = Template(filename=xsd_file.name, content=xsd_data)
        template_version_manager_api.insert(template_version_manager, template)
        return HttpResponseRedirect(reverse("admin:core_main_app_manage_template_versions",
                                            kwargs={'version_manager_id': str(template_version_manager.id)}))
    except exceptions.XSDError, xsd_error:
        return _handle_xsd_errors(request, assets, context, xsd_error, xsd_data, xsd_file.name)
    except Exception, e:
        context['errors'] = html_escape(e.message)
        return _upload_template_response(request, assets, context)


def _handle_xsd_errors(request, assets, context, xsd_error, xsd_content, filename):
    """Handles XSD errors. Builds dependency resolver if needed.

    Args:
        request:
        context:
        xsd_error:
        xsd_content:
        filename:

    Returns:

    """
    imports, includes = get_imports_and_includes(xsd_content)
    # a problem with includes/imports has been detected
    if len(includes) > 0 or len(imports) > 0:
        # build dependency resolver
        context['dependency_resolver'] = _get_dependency_resolver_html(imports, includes, xsd_content,
                                                                       filename)
        return _upload_template_response(request, assets, context)
    else:
        context['errors'] = html_escape(xsd_error.message)
        return _upload_template_response(request, assets, context)


def _read_xsd_file(xsd_file):
    """Returns the content of the file uploaded using Django FileField

    Returns:

    """
    # put the cursor at the beginning of the file
    xsd_file.seek(0)
    # read the content of the file
    return xsd_file.read()


def _upload_template_response(request, assets, context):
    """Renders template upload response

    Args:
        request:
        context:

    Returns:

    """
    return render(request,
                  'core_main_app/admin/upload_template.html',
                  assets=assets,
                  context=context)


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
