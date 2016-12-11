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

    $.ajax({
        url : disableTemplatePostUrl,
        type : "GET",
        data: {
            "id": $("#disable-template-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.delete').on('click', disableTemplate);
    $('#disable-template-yes').on('click', disable_template);
});