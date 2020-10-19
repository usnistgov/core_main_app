/**
 * Create workspace
 */
createWorkspace = function() {
    $("#banner_errors").hide();
    $("#create-workspace-modal").modal("show");
};

/**
 * AJAX call, change record owner
 */
create_workspace = function(){
    var workspaceTitle = $("#id_workspace_name").val().trim();
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
        error:function(data){
            $("#create_workspace_errors").html(data.responseJSON["message"]);
            $("#banner_errors").show(500)
        }
    });
};


$('.create-workspace-btn').on('click', createWorkspace);
$('#create-workspace-yes').on('click', create_workspace);
