/**
 * Edit general information of a template
 */
editTemplateOpenModal = function(event) {
    event.preventDefault();

    var templateName = $(this).parent().siblings(':first').text();
    var templateId = $(this).attr("objectid");

    hideErrorEditTemplate();
    $("#edit-template-name").val(templateName);
    $("#edit-template-id").val(templateId);
    $("#edit-template-modal").modal("show");
};

editTemplateSave = function(event) {
    event.preventDefault();

    var templateId = $("#edit-template-id").val();
    var templateName = $("#edit-template-name").val();

    $.ajax({
        url : editTemplatePostUrl,
        type : "POST",
        data: {
            "id": templateId,
            "title": templateName
        },
        success: function(data){
            location.reload();
        },
        error: function(data){
            showErrorEditTemplate(data.responseText);
        }
    });
};

/*
* Show label error with message
* */
showErrorEditTemplate = function(message){
    $('#error-div-edit-template').show();
    $('#error-message').text(message);
};

/*
* Hide label error with message
* */
hideErrorEditTemplate = function(){
    $('#error-div-edit-template').hide();
    $('#error-message').text('');
};

$(document).ready(function() {
    $('.edit').on('click', editTemplateOpenModal);
    $('.edit-template-btn').on('click', editTemplateOpenModal);
    $('#edit-template-form').on('submit', editTemplateSave);
    $('#edit-template-save').on('click', editTemplateSave);
});
