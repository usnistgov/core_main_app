
/**
 * AJAX call
 */
load_form_add_group = function() {
    $("#add-group-modal").modal("show");
    $('#add-group-yes').show();

    $.ajax({
        url : editGroupRightFormsUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id
        },
		success: function(data){
            $("#banner_rights_errors").hide();
            $("#add-group-form").html(data.form);
            InitSelectMultipleUsersOrGroups("#add-group-form #id_groups", "Groups");
	    },
        error:function(data){
            $("#form_edit_group_rights_errors").html(data.responseText);
            $("#banner_group_rights_errors").show(500);
            $('#add-group-yes').hide();
        }
    });
};

add_group_from_form = function() {
var selected = [];
var select=document.getElementById("id_groups");
var read = document.getElementById("read_group").checked;
var write = document.getElementById("write_group").checked;

for (var i = 0; i < select.options.length; i++) {
 if (select.options[i].selected == true) {
      selected.push(select.options[i].value);
  }
}
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
