""" Urls utils
"""

import re

from django.urls import reverse


def get_template_download_pattern():
    """ Return regex pattern to match an url to download a template.

    Returns:

    """
    # build django url to download a template
    download_template_url = reverse('core_main_app_rest_template_download', kwargs={'pk': 'template_id'})
    # make url a regex
    download_template_regex = download_template_url.replace('template_id', '(?P<pk>\w+)')
    # compile regex
    pattern = re.compile(download_template_regex)

    return pattern
