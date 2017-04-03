
$(document).ready(function() {
    $('#btn-previous-page').on('click',backToPreviousPage);
});


function backToPreviousPage() {
    window.history.back();
}