
$(document).ready(function() {
    $('#btn-previous-page').on('click',backToPreviousPage);
});


function backToPreviousPage() {
    window.history.back();
}

runDataProcessingModule = function(event) {
    event.preventDefault();

    let $data_processing_module_select = $("#data_processing_module_select");
    let processing_module_id = $data_processing_module_select.val();
    let processing_module_name = $data_processing_module_select
        .find('option:selected')
        .text();
    let data_id = $("#data_id").html();
    if (processing_module_id === null || processing_module_id == 'None') {
        notify("Please select a module to first.", "error");
        return;
    }
    console.log(processing_module_id);
    $.ajax({
        url : processDataUrl
            .replace("data_id", data_id)
            .replace("processing_module_id", processing_module_id),
        type : "POST",
        dataType: "json",
        success: function(data){
            notify("Data processing started!", "success");
        },
        error:function(data){
            notify(`Error while triggering module '${processing_module_name}' for the current file.`, "error");
        }
    });
};
$('#btn-run').on('click', runDataProcessingModule);

var redirectToTextEditor = function(openUrl, selector, param) {
    var icon = selector.find( "i" ).attr("class");
    var objectID = $("#data_id").html();
    showSpinner(selector.find("i"))
    window.location = openUrl + '?'+param+'=' + objectID;
    hideSpinner(selector.find("i"), icon)
};

/**
 * Get the URL to go to the edit page
 */
var openEditRecord = function() {
    var objectID = $("#data_id").html();
    var editBtn = $(this).find( "i" ).attr("class");
    var icon = $(editBtn).attr("class");

    // Show loading spinner
    showSpinner($(this).find("i"));
    $.ajax({
        url : editRecordUrl,
        type : "POST",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            window.location = data.url;
        },
        error:function(data){
            let jsonResponse = JSON.parse(data.responseText);
            $.notify(jsonResponse.message, "danger");
        }
    }).always(function() {
        // get old button icon
        hideSpinner(editBtn, icon)
    });
};

$(".edit-record-btn").on('click', openEditRecord);

$(".open-xml-record-btn").on('click',function() {
    redirectToTextEditor(openXMLRecordUrl, $(this), "id")
});

$(".open-json-record-btn").on('click',function() {
    redirectToTextEditor(openJSONRecordUrl, $(this), "id")
});
