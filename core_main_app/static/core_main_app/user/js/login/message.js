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
    // set up the modal
    $("#login-modal-id").modal({
        show: true,
        keyboard: false,
        backdrop: 'static',
    });
    // hide the '+' of the modal
    $(".close").hide();
    // binding event to cancel/yes buttons
    $("#btn-login-cancel").on("click", redirect_to_home);
    $("#btn-login-yes").on("click", hide_modal);
});

