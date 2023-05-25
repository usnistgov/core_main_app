/**
 * Set current version
 */
setCurrentVersion = function(){
    var objectID = $(this).attr("objectid");
    set_current_version(objectID);
}

/**
 * AJAX call, sets the current version
 * @param objectID id of the object
 */
set_current_version = function(objectID){
    $.ajax({
        url : setCurrentVersionPostUrl.replace('template_version_id', objectID),
        type : "PATCH",
        success: function(data){
            location.reload();
        },
        error:function(data){
            $.notify(data.responseJSON["message"], "danger");
        }
    });
};

$(document).ready(function() {
    $('.current').on('click', setCurrentVersion);
});