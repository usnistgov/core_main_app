"""
# File Name: models.py
# Application: mgi
# Description:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#         Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
"""

# Anonymous group
anonymous_group = "anonymous"
#######################

# Default group
default_group = "default"
#######################

# API rights
api_content_type = "api"
api_access = "api_access"
#######################


def get_description(right):
    """ Return the description of a specific right

    :param right:
    :return:
    """
    return "Can " + right.replace("_", " ")
