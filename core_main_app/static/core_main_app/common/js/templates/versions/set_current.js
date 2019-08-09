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
        url : setCurrentVersionPostUrl,
        type : "GET",
        data: {
            id: objectID
        },
        success: function(data){
            location.reload();
        },
        error:function(data){
            $.notify(data.responseText);
        }
    });
};

$(document).ready(function() {
    $('.current').on('click', setCurrentVersion);
});