$(document).ready(function() {
    $('#btn-dismiss-modal').on('click', hideErrorModal);
});

/**
 * Display the error modal and fill the message
 */
function showErrorModal(error_message){
    $('#modal-error-message').html(error_message);
    $('#error-modal').modal("show");
}

/**
 * Hide the error modal and reset the message
 */
function hideErrorModal(){
    $('#modal-error-message').html('');
    $('#error-modal').modal("hide");
}