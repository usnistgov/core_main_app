/**
 * Restores a version
 */
restoreVersion = function()
{
    var objectID = $(this).attr("objectid");
    restore_version(objectID);
}


/**
 * AJAX call, restores a version
 * @param objectID id of the object
 */
restore_version = function(objectID){
    $.ajax({
        url : restoreVersionPostUrl.replace("template_version_id", objectID),
        type : "PATCH",
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.retrieve').on('click', restoreVersion);
});