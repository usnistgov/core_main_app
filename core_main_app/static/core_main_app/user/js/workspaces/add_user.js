
/**
 * AJAX call
 */
load_form_add_user = function() {
    $("#banner_rights_errors").hide();
    $("#user-rights").show()
    $('#add-user-yes').show();
    $("#add-user-modal").modal("show");

    $.ajax({
        url : editUserRightFormsUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id
        },
		success: function(data){
            $("#add-user-form").html(data.form);
	    },
        error:function(data){
            $("#form_edit_rights_errors").html(data.responseText);
            $("#banner_rights_errors").show(500);
            $("#user-rights").hide();
            $('#add-user-yes').hide();
        }
    });
};

add_user_from_form = function() {
    var selected = new FormData($("#add-user-form")[0]).getAll("users");
    var read = document.getElementById("read").checked;
    var write = document.getElementById("write").checked;
    call_ajax_add_user(selected, read, write)
};

call_ajax_add_user = function(selected, read, write) {
    event.preventDefault()
    $("#banner_rights_errors").hide();
    $("#form_edit_rights_errors").html("");
    $.ajax({
        url : addUserToWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            users_id: selected,
            read: read,
            write: write
        },
        success: function(data){
           location.reload();
        },
        error:function(data){
            $("#form_edit_rights_errors").html(data.responseText);
            $("#banner_rights_errors").show(500);
        }
    });
};

$('.add-user-btn').on('click', load_form_add_user);
$('#add-user-yes').on('click', add_user_from_form);
