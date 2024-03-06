
/**
 * Show spinner for button
 */
var showSpinner = function($btnID) {
     // Show loading spinner
     $btnID.attr('class','fas fa-spinner fa-pulse');
     var dropdown = $("#dropdownActions");
     if (dropdown){
           $(dropdown).find( "i" ).attr("class","fas fa-spinner fa-pulse");
     }
}

/**
 *  Hide spinner for button
 */
var hideSpinner = function($btnID,icon) {
    // show old btn icon
    $btnID.attr('class',icon)
    var dropdown = $("#dropdownActions");
    if (dropdown){
         $(dropdown).find( "i" ).attr('class',"fas fa-sliders")
    }
}


/**
 * Show spinner for container
 */
var displaySpinner = function(container) {
     // clear container
     container.html("");
     // display loading spinner
     container.append($("<i class='fa fa-spinner fa-pulse fa-3x fa-fw loading-spinner'></i>"));
}

/**
 * Remove spinner from container
 */
var removeSpinner = function(container) {
    container.find('.loading-spinner').remove();
}