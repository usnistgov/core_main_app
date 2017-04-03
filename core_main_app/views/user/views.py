""" Core main app user views
"""
from core_main_app.utils.rendering import render
import core_main_app.components.data.api as data_api


def data_detail(request):
    """

    Args:
        request:

    Returns:

    """
    data_id = request.GET['id']

    try:
        data = data_api.get_by_id(data_id)
    except:
        # TODO: catch good exception, redirect to error page
        pass

    context = {
        'data': data
    }

    assets = {
        "js": [
            {
                "path": 'core_main_app/common/js/XMLTree.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/user/js/data/detail.js',
                "is_raw": False
            },
        ],
        "css": ["core_main_app/common/css/XMLTree.css"],
    }

    return render(request, 'core_main_app/user/data/detail.html', context=context, assets=assets)
