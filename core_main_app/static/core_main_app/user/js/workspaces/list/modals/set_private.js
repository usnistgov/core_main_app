/**
 * Private workspace
 */
setPrivateWorkspace = function() {
    $("#banner_errors").hide();
    var $recordRow = $(this).parent().parent();
    $('.'+functional_object+'-id').val($recordRow.attr("objectid"));
    $("#private-workspace-modal").modal("show");
};

/**
 * AJAX call, private workspace
 */
set_private_workspace = function(){
    $.ajax({
        url : privateWorkspaceUrl.replace("workspace_id", getSelectedDocument()),
        type : "PATCH",
		success: function(data){
			location.reload();
	    },
        error:function(data){
            $("#private_workspace_errors").html(data.responseText);
            $("#banner_errors").show(500)
        }
    });
};


$('.private-workspace-btn').on('click', setPrivateWorkspace);
$('#private-workspace-yes').on('click', set_private_workspace);
