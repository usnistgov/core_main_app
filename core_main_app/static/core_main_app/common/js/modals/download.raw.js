var downloadXmlUrl = "{% url 'core_main_app_rest_data_download' data.data.id  %}";
var downloadXsdUrl = "{% url 'core_main_app_rest_template_download' data.data.template.id  %}";