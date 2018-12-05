/**
 * Public workspace
 */
setPublicWorkspace = function() {
    $("#banner_set_public_errors").hide();
    var $recordRow = $(this).parent().parent();
    $('.'+functional_object+'-id').val($recordRow.attr("objectid"));
    $("#public-workspace-modal").modal("show");
};

/**
 * AJAX call, public workspace
 */
set_public_workspace = function(){
    $.ajax({
        url : publicWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: getSelectedDocument()
        },
		success: function(data){
			location.reload();
	    },
        error:function(data){
            $("#set_public_workspace_errors").html(data.responseText);
            $("#banner_set_public_errors").show(500)
        }
    });
};


$('.public-workspace-btn').on('click', setPublicWorkspace);
$('#public-workspace-yes').on('click', set_public_workspace);
