/**
 * Edit general information of a xslt
 */
editXSLTOpenModal = function(event) {
    event.preventDefault();

    var xsltName = $(this).parent().siblings(':first').text();
    var $xsltRow = $(this).parent().parent();
    var xsltId = $xsltRow.attr("objectid");

    $("#edit-xslt-name").val(xsltName);
    $("#edit-xslt-id").val(xsltId);
    $("#edit-xslt-modal").modal("show");
}

editXSLTSave = function(event) {
    event.preventDefault();

    var xsltId = $("#edit-xslt-id").val();
    var xsltName = $("#edit-xslt-name").val();

    $.ajax({
        url : editXSLTPostUrl,
        type : "POST",
        data: {
            "id": xsltId,
            "name": xsltName
        },
        success: function(data){
            location.reload();
        },
        error: function(data){
        }
    });
}

$(document).ready(function() {
    $('.edit-xslt-btn').on('click', editXSLTOpenModal);
    $('#edit-xslt-form').on('submit', editXSLTSave);
    $('#edit-xslt-save').on('click', editXSLTSave);
});
