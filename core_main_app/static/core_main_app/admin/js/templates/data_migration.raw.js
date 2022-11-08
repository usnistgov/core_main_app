let loadDataUrlBase = "{% url 'core_main_app_rest_data_query' %}";
let migrationUrlBase = "{% url 'core_main_app_rest_data_migrate' pk='placeholder_id' %}";
let taskBaseUrl = "{% url 'core_main_app_rest_data_migration_task_progress' task_id='placeholder_id' %}";
let versionManagerUrlBase = "{% url 'core-admin:core_main_app_manage_template_versions' version_manager_id='version_manager_id'%}";
let loadAllTemplateUrlBase = "{% url 'core_main_app_rest_all_template_version_manager_list' %}";
let loadGlobalTemplateUrlBase = "{% url 'core_main_app_rest_template_version_manager_global_list' %}";