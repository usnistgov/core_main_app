/**
 * Disable a template
 */
disableTemplate = function()
{
    var objectID = $(this).attr("objectid");

    $(function() {
        $( "#dialog-disable-confirm-message" ).dialog({
            modal: true,
            buttons: {
		Yes: function() {
					disable_template(objectID);
                    $( this ).dialog( "close" );
                },
		No: function() {
                    $( this ).dialog( "close" );
                }
	        }
        });
    });
}

/**
 * AJAX call, delete a template
 * @param objectID id of the object
 */
disable_template = function(objectID){
    $.ajax({
        url : "/admin/template/disable?id=" + objectID,
        type : "GET",
        success: function(data){
            location.reload();
        }
    });
}

/**
 * Restore a template
 */
restoreTemplate = function()
{
    var objectID = $(this).attr("objectid");
    restore_template(objectID);
}


/**
 * AJAX call, restores an object
 * @param objectID id of the object
 */
restore_template = function(objectID){
    $.ajax({
        url : "/admin/template/restore?id=" + objectID,
        type : "GET",
        success: function(data){
            location.reload();
        }
    });
}


/**
 * Disable a version
 */
disableVersion = function()
{
    var objectID = $(this).attr("objectid");

    $(function() {
        $( "#dialog-disable-confirm-message" ).dialog({
            modal: true,
            buttons: {
		Yes: function() {
					disable_version(objectID);
                    $( this ).dialog( "close" );
                },
		No: function() {
                    $( this ).dialog( "close" );
                }
	        }
        });
    });
}

/**
 * AJAX call, deletes a version
 * @param objectID id of the object
 */
disable_version = function(objectID){
    $.ajax({
        url : "/admin/template/version/disable?id=" + objectID,
        type : "GET",
        success: function(data){
            location.reload();
        }
    });
}

/**
 * Restores a version
 */
restoreVersion = function()
{
    var objectID = $(this).attr("objectid");
    restore_version(objectID);
}


/**
 * AJAX call, restores a version
 * @param objectID id of the object
 */
restore_version = function(objectID){
    $.ajax({
        url : "/admin/template/version/restore?id=" + objectID,
        type : "GET",
        success: function(data){
            location.reload();
        }
    });
}


/**
 * Resolve dependencies
 */
resolveDependencies = function()
{
    var schemaLocations = []
	var dependencies = [];

	$("#dependencies").find("tr:not(:first)").each(function(){
        schemaLocation = $(this).find(".schemaLocation").html();
        dependency = $(this).find(".dependency").val();
        schemaLocations.push(schemaLocation)
        dependencies.push(dependency);
    });

    var xsd_content = $("#xsd_content").html();
    var name = $("#id_name").val();
    var filename = $("#filename").html();
    var version_manager_id = $("#vm_id").html();
	resolve_dependencies(xsd_content, name, filename, version_manager_id, schemaLocations, dependencies);
}


/**
 * AJAX call, resolves dependencies
 * @param dependencies
 */
resolve_dependencies = function(xsd_content, name, filename, version_manager_id, schemaLocations, dependencies){
    $.ajax({
        url : "/admin/template/resolve-dependencies",
        type : "POST",
        dataType: "json",
        data : {
            xsd_content: xsd_content,
            name: name,
            filename: filename,
            version_manager_id: version_manager_id,
            schemaLocations: schemaLocations,
        	dependencies : dependencies,
        },
        success: function(data){
            var redirect = $("#redirect_url").html();
            window.location = redirect;
        },
        error: function(data){
            $("#errorDependencies").html(data.responseText);
        }
    });
}


/**
 * Edit general information of a template
 */
editInformation = function()
{
    var objectName = $(this).parent().siblings(':first').text();
    var objectID = $(this).attr("objectid");

    $("#edit-name")[0].value = objectName;

	$(function() {
        $( "#dialog-edit-info" ).dialog({
            modal: true,
            buttons: {
            	Ok: function() {
					var newName = $("#edit-name")[0].value;
					edit_information(objectID, newName);
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}


/**
 * AJAX call, edit information of an object
 * @param objectID id of the object
 * @param newName new name of the object
 */
edit_information = function(objectID, newName){
    $.ajax({
        url : "/admin/template/edit?id=" + objectID + "&title=" + newName,
        type : "GET",
        success: function(data){
            location.reload();
        },
        error: function(data){

        }
    });
}

/**
 * Set current version
 */
setCurrentVersion = function(){
    var objectID = $(this).attr("objectid");
    set_current_version(objectID);
}

/**
 * AJAX call, sets the current version
 * @param objectID id of the object
 */
set_current_version = function(objectID){
    $.ajax({
        url : "/admin/template/version/current?id=" + objectID,
        type : "GET",
        success: function(data){
            location.reload();
        }
    });
}
