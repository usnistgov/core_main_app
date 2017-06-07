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
    hideErrorXSLT();
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
            showErrorXSLT(data.responseText);
        }
    });
}

/*
* Show label error with message
* */
showErrorXSLT = function(message){
    $('#error-div-xslt').show();
    $('#error-message').text(message);
};

/*
* Hide label error with message
* */
hideErrorXSLT = function(message){
    $('#error-div-xslt').hide();
    $('#error-message').text('');
};


$(document).ready(function() {
    $('.edit-xslt-btn').on('click', editXSLTOpenModal);
    $('#edit-xslt-form').on('submit', editXSLTSave);
    $('#edit-xslt-save').on('click', editXSLTSave);
});
