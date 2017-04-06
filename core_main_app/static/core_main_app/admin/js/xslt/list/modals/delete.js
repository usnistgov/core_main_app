/**
 * Delete a XSLT
 */
deleteXslt = function(event)
{
    event.preventDefault();

    var $xsltRow = $(this).parent().parent();
    var objectID = $xsltRow.attr("objectid");
    var xsltName = $xsltRow.find("td:first").text();

    $(".delete-xslt-name").text(xsltName);
    $("#delete-xslt-id").val(objectID);
    $("#delete-xslt-modal").modal("show");
}

/**
 * AJAX call, delete a template
 * @param objectID id of the object
 */
delete_xslt = function(event){
    event.preventDefault();

    $.ajax({
        url : deleteXSLTPostUrl,
        type : "POST",
        data: {
            "id": $("#delete-xslt-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.delete-xslt-btn').on('click', deleteXslt);
    $('#delete-xslt-yes').on('click', delete_xslt);
});