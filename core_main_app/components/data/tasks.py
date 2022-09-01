""" Data tasks
"""

import logging

from celery import shared_task
from celery.result import AsyncResult
from django.db.models import Q

from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.xsl_transformation import api as xsl_transformation_api
from core_main_app.system import api as system_api

logger = logging.getLogger(__name__)


@shared_task
def async_migration_task(data_list, xslt_id, template_id, user_id, migrate):
    """Async task which perform a migration / validation of the data list for the given target template id

    Args:
        data_list:
        xslt_id:
        template_id:
        user_id:
        migrate: (boolean) Perform the migration

    Return:
        {"valid": ["id"...], "wrong": ["id"...]}
    """
    success = []
    errors = []
    current_progress = 0
    total_data = len(data_list)

    try:
        user = user_api.get_user_by_id(user_id)
        target_template = system_api.get_template_by_id(template_id)

        # get xsl transformation if selected
        if xslt_id is not None:
            xslt = xsl_transformation_api.get_by_id(str(xslt_id))

        for data_id in data_list:
            data = data_api.get_by_id(data_id, user=user)
            # modify the data temporarily with the new targeted template
            data.template = target_template

            if xslt_id is not None:
                # modify the xml content temporarily with the transformed data content
                data.xml_content = xsl_transformation_api.xsl_transform(
                    data.xml_content, xslt.name
                )

            try:
                # save the new template for the data if the migration is True
                if migrate:
                    system_api.upsert_data(data)
                else:
                    # check if the data is valid
                    data_api.check_xml_file_is_valid(data)

                success.append(str(data.id))
            except Exception:
                errors.append(str(data.id))
            finally:
                # increase the current progress and update the task state
                current_progress += 1
                async_migration_task.update_state(
                    state="PROGRESS",
                    meta={"current": current_progress, "total": total_data},
                )
    except Exception as exception:
        async_migration_task.update_state(
            state="ABORT", meta={"current": current_progress, "total": total_data}
        )
        raise Exception(f"Something went wrong: {str(exception)}")

    return {"valid": success, "wrong": errors}


@shared_task
def async_template_migration_task(
    templates, xslt_id, target_template_id, user_id, migrate
):
    """Async task which perform a migration / validation of all the data which belong to the given template id list

    Args:
        templates:
        xslt_id:
        target_template_id:
        user_id
        migrate: (boolean) Perform the migration

    Return:
        {"valid": <number>, "wrong": <number>}
    """
    # get the data list to check
    current_data_progress = 0
    current_template_progress = -1
    total_data = 0
    total_template = len(templates)
    success = []
    error = []
    try:
        if target_template_id and total_template > 0:
            # get the user
            user = user_api.get_user_by_id(user_id)
            # get the target template
            target_template = system_api.get_template_by_id(target_template_id)
            # get xsl transformation if selected
            if xslt_id is not None:
                xslt = xsl_transformation_api.get_by_id(str(xslt_id))

            for template_id in templates:

                # increase the number of processed template
                current_template_progress += 1
                # rest de number of data
                current_data_progress = 0

                # get a QuerySet of all the data with the given template
                data_list = data_api.execute_query(Q(template=template_id), user=user)

                total_data = data_list.count()

                for data in data_list.all():
                    # modify the data temporarily with the new targeted template
                    data.template = target_template

                    if xslt_id is not None:
                        # modify the xml content temporarily with the transformed data content
                        data.xml_content = xsl_transformation_api.xsl_transform(
                            data.xml_content, xslt.name
                        )

                    # check if the data is valid
                    try:
                        # save the new template for the data if the migration is True
                        if migrate:
                            system_api.upsert_data(data)
                        else:
                            data_api.check_xml_file_is_valid(data)

                        success.append(str(data.id))
                    except Exception:
                        error.append(str(data.id))
                    finally:
                        # increase the current progress and update the task state
                        current_data_progress += 1
                        async_template_migration_task.update_state(
                            state="PROGRESS",
                            meta={
                                "template_current": current_template_progress,
                                "template_total": total_template,
                                "data_current": current_data_progress,
                                "data_total": total_data,
                            },
                        )

            return {"valid": success, "wrong": error}

        else:
            async_template_migration_task.update_state(
                state="ABORT",
                meta={
                    "template_current": current_template_progress,
                    "template_total": total_template,
                    "data_current": current_data_progress,
                    "data_total": total_data,
                },
            )
            raise Exception(
                "Wrong template id."
                if not target_template_id
                else "Please provide template id."
            )
    except Exception as exception:
        async_template_migration_task.update_state(
            state="ABORT",
            meta={
                "template_current": current_template_progress,
                "template_total": total_data,
                "data_current": current_data_progress,
                "data_total": total_data,
            },
        )
        raise Exception(f"Something went wrong: {str(exception)}")


def get_task_progress(task_id):
    """Get task status for the given task id

    Args:
        task_id:

    Return:
        {
            'state': PENDING | PROGRESS | SUCCESS,
            'details': result (for SUCCESS) | null (for PENDING) | { PROGRESS info }
        }
    """
    result = AsyncResult(task_id)
    response_data = {
        "state": result.state,
        "details": result.info,
    }
    return response_data


def get_task_result(task_id):
    """Get task result for the given task id

    Args:
        task_id:

    Return: {
                "valid": ["data_id_1", "data_id_2" ...],
                "wrong": ["data_id_3", "data_id_4" ...]
            }
    """
    result = AsyncResult(task_id).result
    return result


@shared_task
def index_mongo_data(data_id):
    """Index a data in MongoDB"""
    try:
        data = system_api.get_data_by_id(data_id)
        try:
            from core_main_app.components.mongo.models import MongoData

            mongo_data = MongoData.init_mongo_data(data)
            mongo_data.save()
        except Exception as exception:
            logger.error(
                f"ERROR : An error occurred while indexing data : {str(exception)}"
            )
    except Exception as exception:
        logger.error(
            f"ERROR : An error occurred while indexing data : {str(exception)}"
        )


@shared_task
def update_mongo_data_user(data_ids, user_id):
    """Update user id of all data in list

    Args:
        data_ids:
        user_id:

    Returns:

    """
    try:
        from core_main_app.components.mongo.models import MongoData

        for data_id in data_ids:
            mongo_data = MongoData.objects.get(pk=data_id)
            mongo_data.user_id = user_id
            mongo_data.save()
    except Exception as exception:
        logger.error(
            f"ERROR : An error occurred while updating data owner : {str(exception)}"
        )


@shared_task
def update_mongo_data_workspace(data_ids, workspace_id):
    """Update workspace id of all data in list
    Args:
        data_ids:
        workspace_id:

    Returns:

    """

    try:
        from core_main_app.components.mongo.models import MongoData

        for data_id in data_ids:
            mongo_data = MongoData.objects.get(pk=data_id)
            mongo_data._workspace_id = workspace_id
            mongo_data.save()
    except Exception as exception:
        logger.error(
            f"ERROR : An error occurred while updating data workspace : {str(exception)}"
        )


@shared_task
def delete_mongo_data(data_id):
    """Delete a data in MongoDB"""
    try:
        try:
            from core_main_app.components.mongo.models import MongoData

            mongo_data = MongoData.objects.get(pk=data_id)
            mongo_data.delete()
        except Exception as exception:
            logger.error(
                f"ERROR : An error occurred while deleting data : {str(exception)}"
            )
    except Exception as exception:
        logger.error(
            f"ERROR : An error occurred while deleting data : {str(exception)}"
        )
