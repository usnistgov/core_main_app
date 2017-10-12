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
    var name_workspace = $("#id_workspace_name").val().trim();
    $.ajax({
        url : createWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            name_workspace: name_workspace
        },
		success: function(data){
			location.reload();
	    },
        error:function(data){
            $("#create_workspace_errors").html(data.responseText);
            $("#banner_errors").show(500)
        }
    });
};


$('.create-workspace-btn').on('click', createWorkspace);
$('#create-workspace-yes').on('click', create_workspace);
