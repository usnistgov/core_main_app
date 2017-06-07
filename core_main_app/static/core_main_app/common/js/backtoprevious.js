/**
 * Back to previous
 */
backToPrevious = function()
{
    window.history.go(-1);
    return false;
};


/**
 * Load controllers for back to previous
 */
$(document).ready(function() {
    $('.back-to-previous').on('click',backToPrevious);
});
