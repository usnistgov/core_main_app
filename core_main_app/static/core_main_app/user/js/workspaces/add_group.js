
/**
 * AJAX call
 */
load_form_add_group = function() {
    $("#banner_group_rights_errors").hide();
    $('#group-rights').show();
    $('#add-group-yes').show();
    $("#add-group-modal").modal("show");

    $.ajax({
        url : editGroupRightFormsUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id
        },
		success: function(data){
            $("#add-group-form").html(data.form);
	    },
        error:function(data){
            $("#form_edit_group_rights_errors").html(data.responseText);
            $("#banner_group_rights_errors").show(500);
            $('#group-rights').hide();
            $('#add-group-yes').hide();
        }
    });
};

add_group_from_form = function() {
    var selected = new FormData($("#add-group-form")[0]).getAll("groups");;
    var read = document.getElementById("read_group").checked;
    var write = document.getElementById("write_group").checked;

    call_ajax_add_group(selected, read, write)
};

call_ajax_add_group = function(selected, read, write) {
    event.preventDefault()
    $("#banner_group_rights_errors").hide();
    $("#form_edit_group_rights_errors").html("");
    $.ajax({
        url : addGroupToWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            groups_id: selected,
            read: read,
            write: write
        },
        success: function(data){
            location.reload();
        },
        error:function(data){
            $("#form_edit_group_rights_errors").html(data.responseText);
            $("#banner_group_rights_errors").show(500);
        }
    });
};

$('.add-group-btn').on('click', load_form_add_group);
$('#add-group-yes').on('click', add_group_from_form);
