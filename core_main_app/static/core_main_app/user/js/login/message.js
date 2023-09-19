/*
* Javascript file of the web page login
*/

/*
* redirect to home page
*/
var redirect_to_home = function() {
    document.location.href = indexUrl;
}

/*
* hide the modal and make the login page accessible
*/
var hide_modal = function() {
    $("#login-modal-id").modal("hide");
}

$(document).ready(function() {
    const $loginModal = $("#login-modal-id");
    // set up the modal
    $loginModal.modal({
        keyboard: false,
        backdrop: 'static',
    });
    // hide the 'x' of the modal
    $(".close").hide();
    $(".btn-close").hide();
    // binding event to cancel/yes buttons
    $("#btn-login-cancel").on("click", redirect_to_home);
    $("#btn-login-yes").on("click", hide_modal);
    // Display the modal
    $loginModal.modal("show");
});

