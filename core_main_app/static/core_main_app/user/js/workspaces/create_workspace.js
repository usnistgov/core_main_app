/**
 * Create workspace
 */
initCreateWorkspacePopup = function() {
    $("#banner_errors").hide();
    $("#id_workspace_name").val("");
    $("#create-workspace-modal").modal("show");
};

/**
 * AJAX call, change record owner
 */
createWorkspace = function(){
    const workspaceTitle = $("#id_workspace_name").val().trim();
    $.ajax({
        url : createWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            title: workspaceTitle
        },
		success: function(data){
			location.reload();
	    },
        error:function(data) {
            let message;

            if(!data.hasOwnProperty("responseJSON")) {
                message = "An unknown error occured"
            } else {
                if (!(message = data.responseJSON["message"].title)) {
                    message = data.responseJSON["message"]
                }
            }

            $("#create_workspace_errors").html(message);
            $("#banner_errors").show(500)
        }
    });
};

$('.create-workspace-btn').on('click', initCreateWorkspacePopup);
$('#create-workspace-confirm').on('click', createWorkspace);
