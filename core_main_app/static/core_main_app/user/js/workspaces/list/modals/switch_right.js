/**
 * AJAX call to switch right
 */

switch_read_user = function() {
    var $recordRow = $(this).parent().parent().parent();
    call_ajax_switch_right($recordRow.attr("objectid"), action_read,  $(this), "user")
};

switch_write_user = function() {
    var $recordRow = $(this).parent().parent().parent();
    call_ajax_switch_right($recordRow.attr("objectid"), action_write, $(this), "user")
};

switch_read_group = function() {
    var $recordRow = $(this).parent().parent().parent();
    call_ajax_switch_right($recordRow.attr("objectid"), action_read,  $(this), "group")
};

switch_write_group = function() {
    var $recordRow = $(this).parent().parent().parent();
    call_ajax_switch_right($recordRow.attr("objectid"), action_write, $(this), "group")
};

call_ajax_switch_right = function(selected, action, obj, group_or_user) {
    $.ajax({
        url : switchRightUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            object_id: selected,
            action: action,
            value: obj.prop("checked"),
            group_or_user: group_or_user
        },
        success: function(data){},
        error:function(data){
            obj.prop("checked", !obj.prop("checked"));
            $("#switch_rights_errors").html(data.responseText);
            $("#switch_rights_banner_errors").show(50);
            $("#switch-rights-modal").modal("show");
        }
    });
};


$( "input[id*='btn-read-user']" ).on('change', switch_read_user);
$( "input[id*='btn-write-user']" ).on('change', switch_write_user);
$( "input[id*='btn-read-group']" ).on('change', switch_read_group);
$( "input[id*='btn-write-group']" ).on('change', switch_write_group);
