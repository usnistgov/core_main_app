/**
 * Disable a version
 */
disableVersion = function(event)
{
    event.preventDefault();

    var $templateRow = $(this).parent().parent();
    var versionId = $(this).attr("objectid");  // FIXME remove object id from button (put as tr id)
    var versionNumber = $templateRow.find("td:first").text();

    $(".disable-version-number").text(versionNumber);
    $("#disable-version-id").val(versionId);
    $("#disable-version-modal").modal("show");
}

/**
 * AJAX call, deletes a version
 * @param objectID id of the object
 */
disable_version = function(event){
    event.preventDefault();
    templateVersionId = $("#disable-version-modal").find("#disable-version-id").val()
    $.ajax({
        url : disableVersionPostUrl.replace("template_version_id", templateVersionId),
        type : "PATCH",
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.delete').on('click', disableVersion);
    $('#disable-version-yes').on('click', disable_version);
});