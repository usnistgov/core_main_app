/**
 * Resolve dependencies
 */
resolveDependencies = function(event)
{
    event.preventDefault();

    var schemaLocations = []
	var dependencies = [];

	$("#dependencies").find("tr:not(:first)").each(function(){
        schemaLocation = $(this).find(".schemaLocation").text().trim();
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
        url : templateDependenciesPostUrl,
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
 * Load controllers for dependency resolver
 */
$(document).ready(function() {
    $('.resolve').on('click', resolveDependencies);
});
