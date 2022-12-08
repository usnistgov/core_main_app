"""Mongo query builder tools
"""
import copy
import re

from django.conf import settings

from core_main_app.commons.exceptions import QueryError
from core_main_app.utils.databases.backend import uses_postgresql_backend


def _compile_regex(query):
    """Compile all regular expressions in the query

    Args:
        query:

    Returns:

    """
    for key, value in query.items():
        if key == "$and" or key == "$or":
            for sub_value in value:
                _compile_regex(sub_value)
        elif isinstance(value, str) or isinstance(value, str):
            if len(value) >= 2 and value[0] == "/" and value[-1] == "/":
                query[key] = re.compile(value[1:-1])
        elif isinstance(value, dict):
            _compile_regex(value)


def _add_sub_document_root(query, sub_document_root):
    """Adds a sub document root to each criteria

    Returns:

    """
    for key in list(query.keys()):
        if key == "$and" or key == "$or":
            for value in query[key]:
                _add_sub_document_root(value, sub_document_root)
        elif not key.startswith("$"):
            query[f"{sub_document_root}.{key}"] = query.pop(key)


def prepare_query(query_dict, regex=True, sub_document_root=None):
    """Prepares the query to before executing it

    Args:
        query_dict:
        regex:
        sub_document_root:

    Returns:

    """
    # get a copy of the query
    query = copy.deepcopy(query_dict)

    if regex:
        # compile the regular expressions
        _compile_regex(query)

    if sub_document_root is not None:
        # add a sub document root
        _add_sub_document_root(query, sub_document_root)

    return query


def get_access_filters_from_query(
    query_dict, workspace_list=None, user_list=None
):
    """Get workspaces criteria from queries

    Args:
        query_dict:
        workspace_list:
        user_list:

    Returns:

    """
    # create empty list of workspaces if not defined
    workspace_list = [] if not workspace_list else workspace_list
    # create empty list of users if not defined
    user_list = [] if not user_list else user_list
    # iterate through query dict
    for key, value in query_dict.items():
        # if key is workspace
        if key == "workspace":
            # if filter on a list of workspaces
            if (
                isinstance(query_dict["workspace"], dict)
                and "$in" in query_dict["workspace"]
            ):
                # append each workspace id to list of workspaces
                for workspace_id in query_dict["workspace"]["$in"]:
                    workspace_list.append(workspace_id)
            # if filter on a single value
            elif (
                isinstance(query_dict["workspace"], int)
                or isinstance(query_dict["workspace"], str)
                or query_dict["workspace"] is None
            ):
                # add workspace id to the list of workspaces
                workspace_list.append(query_dict["workspace"])
        # if key is user_id
        elif key == "user_id":
            # if filter on a list of user ids
            if (
                isinstance(query_dict["user_id"], dict)
                and "$in" in query_dict["user_id"]
            ):
                # append each user id to list of user ids
                for user_id in query_dict["user_id"]["$in"]:
                    user_list.append(str(user_id))
            # if filter on a single value
            elif isinstance(query_dict["user_id"], int) or isinstance(
                query_dict["user_id"], str
            ):
                # add user id to the list of users
                user_list.append(str(query_dict["user_id"]))
        else:
            # if AND or OR operators found
            if key in ["$and", "$or"]:
                # iterate though sub dict
                for sub_value in value:
                    (
                        sub_workspace_list,
                        sub_user_list,
                    ) = get_access_filters_from_query(
                        sub_value, workspace_list, user_list
                    )
                    # add values found in sub dict to existing lists
                    if sub_workspace_list:
                        workspace_list.extend(sub_workspace_list)
                    if sub_user_list:
                        user_list.extend(sub_user_list)
    # return list of workspaces and users
    return workspace_list, user_list


def convert_to_django(query_dict):
    """Extract criteria from mongodb query and translates them to django ORM

    Returns:

    """
    if settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q

        template_key = "_template_id"
    else:
        from django.db.models import Q

        template_key = "template"

    # check $where operator
    if "$where" in str(query_dict):
        raise QueryError("Unsupported operator found")

    # create a query object
    q_list = Q()
    # iterate through query dict key/value pairs
    for key, value in query_dict.items():
        # if the key is not an operator
        if not key.startswith("$"):
            # check if $ found in key
            if "$" in key:
                raise QueryError("Unsupported $ operator found")
            # ignore workspace and user_id filters (dealt with by acl layer)
            if key in ["workspace", "_workspace_id", "user_id", "_id", "id"]:
                continue
            # if key is template
            elif key == "template":
                # check if filtering by a list
                if (
                    isinstance(query_dict["template"], dict)
                    and "$in" in query_dict["template"]
                ):
                    # add filter by list of templates
                    q_list &= Q(
                        **{
                            f"{template_key}__in": sanitize_value(
                                query_dict["template"]["$in"]
                            )
                        }
                    )
                # check if filtering by single value
                elif isinstance(query_dict["template"], int) or isinstance(
                    query_dict["template"], str
                ):
                    # add filter by value (template id)
                    q_list &= Q(
                        **{
                            template_key: sanitize_value(
                                query_dict["template"]
                            )
                        }
                    )
            else:
                # initialize negate var to invert django queries
                negate = False
                # replace dots by double underscores (django notation)
                key = key.replace(".", "__") if "." in key else key
                # initialize operator
                operator = "exact"
                # check if not operator
                if isinstance(value, dict) and "$not" in value:
                    negate = True
                    # add not to key
                    key = (
                        f"{key}__not"
                        if negate and settings.MONGODB_INDEXING
                        else key
                    )
                    # move value to document in $not
                    value = value["$not"]
                # if value is a regex
                if isinstance(value, re.Pattern):
                    # set regex operator
                    operator = "regex"
                    # set value with regex pattern
                    value = value.pattern
                # if value is None
                elif value is None:
                    # mongo: __exact = None / django: __exact = None
                    value = None
                # if the value is a dict
                elif isinstance(value, dict):
                    # check if ne operator (not equal)
                    if "$ne" in value:
                        # set not equal to create query not
                        negate = True
                        # set ne operator
                        operator = (
                            "ne" if settings.MONGODB_INDEXING else operator
                        )
                        # set value
                        value = value["$ne"]
                    # check if eq operator (equal to)
                    elif "$eq" in value:
                        # set value
                        value = value["$eq"]
                    # check if lt operator (less than)
                    elif "$lt" in value:
                        # set lt operator
                        operator = "lt"
                        # set value
                        value = sanitize_number(value["$lt"])
                    # check if lt operator (less than or equal)
                    elif "$lte" in value:
                        # set lte operator
                        operator = "lte"
                        # set value
                        value = sanitize_number(value["$lte"])
                    # check if gt operator (greater than)
                    elif "$gt" in value:
                        # set gt operator
                        operator = "gt"
                        # set value
                        value = sanitize_number(value["$gt"])
                    # check if gte operator (greater than or equal)
                    elif "$gte" in value:
                        # set gte operator
                        operator = "gte"
                        # set value
                        value = sanitize_number(value["$gte"])
                    # check if in operator (included in list)
                    elif "$in" in value:
                        # set in operator
                        operator = "in"
                        # set value
                        value = value["$in"]
                    # check if regex operator
                    elif "$regex" in value:
                        # set regex operator
                        operator = "regex"
                        # set the value
                        value = value["$regex"]
                    # check if exists operator
                    elif "$exists" in value:
                        # skip case where set to False for now (i.e. can not look for documents where path is absent)
                        if value["$exists"] is False:
                            raise QueryError(
                                'Unsupported operator found: {"$exists": False}'
                            )
                        if settings.MONGODB_INDEXING:
                            # set exists operator
                            operator = "exists"
                            value = True
                        else:
                            # value to look for is the last element of the key
                            # (e.g. if key is dict_content__root__element, value becomes element)
                            value = key.split("__")[-1]
                            # key is the rest of the path, minus the last part that was just set as value
                            # (e.g. dict_content__root__element, key is dict_content__root)
                            key = "__".join(key.split("__")[:-1])
                            # add has key operator to key (e.g. dict_content__root, becomes dict_content__root__has_key)
                            operator = "has_key"
                    else:
                        # If an operator not listed above is found, an exception is raised
                        raise QueryError(
                            f"Unsupported operator found: {value}"
                        )
                # build query
                query = Q(**{f"{key}__{operator}": sanitize_value(value)})
                # invert django query if negate is true
                query = (
                    ~query
                    if negate and not settings.MONGODB_INDEXING
                    else query
                )

                # add AND query filter from string key and value
                q_list &= query
        else:
            # if operator and
            if key == "$and":
                # iterate though sub dict
                for sub_value in value:
                    # add AND filters to the query
                    q_list &= convert_to_django(sub_value)
            # if operator or
            elif key == "$or":
                # iterate through sub dict
                for sub_value in value:
                    # add OR filters to the query
                    q_list |= convert_to_django(sub_value)
            # if operators text and search found
            elif key == "$text" and "$search" in value:
                # get text query
                text_query = query_dict["$text"]["$search"]
                # check text query is a string
                if not isinstance(text_query, str):
                    raise QueryError(f"Unsupported value found in: {key}")
                # strip white spaces
                text_query = text_query.strip()
                # sanitize string
                sanitize_value(text_query)
                # if data stored in MongoDB
                if settings.MONGODB_INDEXING:
                    q_list &= Q(__raw__={"$text": {"$search": text_query}})
                # if data stored in PostgreSQL
                elif uses_postgresql_backend():
                    q_list &= Q(vector_column=text_query)
                else:
                    # extract keywords from dict
                    for keyword in text_query.split(" "):
                        # add text filter
                        q_list &= Q(
                            dict_content__icontains=keyword.replace('"', "")
                        )
            else:
                # raise an error if another operator was found
                raise QueryError(f"Unsupported operator found: {key}")

    return q_list


def sanitize_number(value):
    """Sanitize number


    Args:
        value:

    Returns:

    """
    # check type of value
    if not (isinstance(value, (int, float))):
        raise QueryError("Unsupported value: expected a number.")
    return value


def sanitize_value(value):
    """Sanitize value

    Args:
        value:

    Returns:

    """
    # check if operator in value
    if "$" in str(value):
        raise QueryError("Unsupported $ operator found.")
    # if value is a list
    if isinstance(value, list):
        # check for $ sign in the list
        for item in value:
            sanitize_value(item)
    return value
