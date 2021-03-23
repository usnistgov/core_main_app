/**
 * Remove rights
 */
removeRightsUser = function() {
    $("#remove_rights_banner_errors").hide();
    var $recordRow = $(this).parent().parent();
    $('.remove-rights-id').val($recordRow.attr("objectid"));
    $('.remove-rights-group-or-user').val("user");
    $("#remove-rights-modal").modal("show");
};

removeRightsGroup = function() {
    $("#remove_rights_banner_errors").hide();
    var $recordRow = $(this).parent().parent();
    $('.remove-rights-id').val($recordRow.attr("objectid"));
    $('.remove-rights-group-or-user').val("group");
    $("#remove-rights-modal").modal("show");
};

/**
 * AJAX call, remove rights
 */
remove_rights = function(type) {
    event.preventDefault()
    $.ajax({
        url : removeRightsUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            object_id: $('.remove-rights-id').val(),
            group_or_user: $('.remove-rights-group-or-user').val()
        },
		success: function(data){
			location.reload();
	    },
        error:function(data){
            $("#remove_rights_errors").html(data.responseText);
            $("#remove_rights_banner_errors").show(500)
        }
    });
};

$('.remove-user-btn').on('click', removeRightsUser);
$('.remove-group-btn').on('click', removeRightsGroup);
$('#remove-yes').on('click', remove_rights);
