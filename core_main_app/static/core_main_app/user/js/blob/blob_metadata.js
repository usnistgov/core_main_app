/**
 * AJAX call
 */
load_form_add_metadata = function() {
    $("#add-metadata-modal").modal("show");

    $.ajax({
        url : blobMetadataFormUrl,
        type : "GET",
        dataType: "json",
        data : {
            blob_id: $("#blob_id").html()
        },
		success: function(data){
            $("#add-metadata").html(data.form);
	    },
        error:function(data){
        }
    });
};

add_metadata_from_form = function() {
    var selected = new FormData($("#add-metadata-form")[0]).getAll("metadata");

    event.preventDefault()
    $.ajax({
        url : addMetadataToBlobUrl,
        type : "POST",
        dataType: "json",
        data : {
            blob_id: $("#blob_id").html(),
            metadata_id: selected,
        },
        success: function(data){
           location.reload();
        },
        error:function(data){
        }
    });
};

remove_metadata = function() {
    event.preventDefault()
    metadata_id = $(event.target).attr("objectid");
    $.ajax({
        url : removeMetadataFromBlobUrl,
        type : "POST",
        dataType: "json",
        data : {
            blob_id: $("#blob_id").html(),
            metadata_id: metadata_id,
        },
        success: function(data){
           location.reload();
        },
        error:function(data){
        }
    });
};


$('.add-metadata-btn').on('click', load_form_add_metadata);
$('.remove-metadata-btn').on('click', remove_metadata);
$('#add-metadata-yes').on('click', add_metadata_from_form);