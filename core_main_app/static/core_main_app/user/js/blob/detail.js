function backToPreviousPage() {
    window.history.back();
}

runBlobProcessingModule = function(event) {
    event.preventDefault();

    let $blob_processing_module_select = $("#blob_processing_module_select");
    let processing_module_id = $blob_processing_module_select.val();
    let processing_module_name = $blob_processing_module_select
        .find('option:selected')
        .text();
    let blob_id = $("#blob_id").html();

    $.ajax({
        url : processFileUrl
            .replace("blob_id", blob_id)
            .replace("processing_module_id", processing_module_id),
        type : "POST",
        dataType: "json",
        success: function(data){
            notify("File processing started!", "success");
        },
        error:function(data){
            notify(`Error while triggering module '${processing_module_name}' for the current file.`, "error");
        }
    });
};

$('#btn-previous-page').on('click', backToPreviousPage);
$('#btn-run').on('click', runBlobProcessingModule);
