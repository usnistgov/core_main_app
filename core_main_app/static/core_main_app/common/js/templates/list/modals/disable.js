/**
 * Disable a template
 */
disableTemplate = function(event)
{
    event.preventDefault();

    var $templateRow = $(this).parent().parent();
    var objectID = $(this).attr("objectid"); // FIXME remove object id from button (put as tr id)
    var templateName = $templateRow.find("td:first").text();

    $(".disable-template-name").text(templateName);
    $("#disable-template-id").val(objectID);
    $("#disable-template-modal").modal("show");
}

/**
 * AJAX call, delete a template
 * @param objectID id of the object
 */
disable_template = function(event){
    event.preventDefault();

    templateVersionManagerId = $("#disable-template-id").val()
    $.ajax({
        url : disableTemplatePostUrl.replace("template_version_manager_id", templateVersionManagerId),
        type : "PATCH",
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.delete').on('click', disableTemplate);
    $('.disable-template-btn').on('click', disableTemplate);
    $('#disable-template-yes').on('click', disable_template);
});