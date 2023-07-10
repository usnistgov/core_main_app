
/**
 * AJAX call
 */
load_form_change_workspace = function() {
    $("#assign-workspace-modal").modal("show");
    var $recordRow = $(this).parent().parent();

    // Get parent if btn in dropdown  (object id undefined)
    if (!$recordRow.attr("objectid")) $recordRow = $recordRow.parent()
    $('.'+functional_object+'-id').val($recordRow.attr("objectid"));

    $.ajax({
        url : changeWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            document_id: getSelectedDocument(),
            administration: administration
        },
		success: function(data){
            $("#banner_assign_workspace_errors").hide();
            $("#assign-workspace-form").html(data.form);
	    },
        error:function(data){
            $("#form_assign_workspace_errors").html(data.responseText);
            $("#banner_assign_workspace_errors").show(500);
        }
    });
};

assign_workspace = function() {
var workspace_id = $( "#id_workspaces" ).val().trim();
$.ajax({
        url : assignWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            document_id: getSelectedDocument()
        },
		success: function(data){
           location.reload();
	    },
        error:function(data){
            $("#form_assign_workspace_errors").html(data.responseText);
            $("#banner_assign_workspace_errors").show(500);
        }
    });
};



$('.assign-workspace-record-btn').on('click', load_form_change_workspace);
$('#assign-workspace-yes').on('click', assign_workspace);