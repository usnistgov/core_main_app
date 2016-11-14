/**
 * Load controllers for template management
 */
$(document).ready(function() {
    $('.edit').on('click', editInformation);
    $('.delete').on('click', disableTemplate);
    $('.retrieve').on('click',restoreTemplate);
});
