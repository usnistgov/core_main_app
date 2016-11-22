/**
 * Load controllers for template version management
 */
$(document).ready(function() {
    $('.delete').on('click', disableVersion);
    $('.retrieve').on('click', restoreVersion);
    $('.current').on('click', setCurrentVersion);
});