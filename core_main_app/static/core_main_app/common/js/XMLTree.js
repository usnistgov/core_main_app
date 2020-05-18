/**
 * Shows/hides a section of the XSD tree
 * @param event
 */
showhide = function(event){
	button = event.target;
	parent = $(event.target).parent();
	$(parent.children('ul')).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse show");
	}else{
		$(button).attr("class","expand");
	}
};