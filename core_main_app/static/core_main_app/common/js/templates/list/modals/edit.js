/**
 * Edit general information of a template
 */
editTemplateOpenModal = function(event) {
    event.preventDefault();

    var templateName = $(this).parent().siblings(':first').text();
    var templateId = $(this).attr("objectid");

    $("#edit-template-name").val(templateName);
    $("#edit-template-id").val(templateId);
    $("#edit-template-modal").modal("show");
}

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

        }
    });
}

$(document).ready(function() {
    $('.edit').on('click', editTemplateOpenModal);
    $('.edit-template-btn').on('click', editTemplateOpenModal);
    $('#edit-template-form').on('submit', editTemplateSave);
    $('#edit-template-save').on('click', editTemplateSave);
});
