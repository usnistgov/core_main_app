
/**
 * Show spinner for button
 */
var showSpinner = function($btnID) {
     // Show loading spinner
     $btnID.attr('class','fas fa-spinner fa-pulse');
}

/**
 *  Hide spinner for button
 */
var hideSpinner = function($btnID,icon) {
    // show old btn icon
    $btnID.attr('class',icon)
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

