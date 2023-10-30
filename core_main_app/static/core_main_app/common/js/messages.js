let notify = function(toastText, toastSeverity) {
    let $toastTemplate = $(".toast-template");
    let $newToast = $toastTemplate.clone();
    let $newToastIcon = $newToast.find(".toast-icon>.fas");
    let $newToastText = $newToast.find(".toast-text");

    // Configure the new toast with the proper content.
    $newToast.removeClass("toast-template");
    $newToast.appendTo($(".toast-container"));
    $newToastText.text(toastText);

    switch (toastSeverity) {  // Change the icon depending on the severity.
        case "info":
            $newToastIcon.addClass("fa-question-circle");
            break;
        case "success":
            $newToastIcon.addClass("fa-check-circle");
            break;
        case "warning":
            $newToastIcon.addClass("fa-exclamation-triangle");
            break;
        case "danger":
        case "error":
            // Messages with "danger" or "error" severity are parsed the same way.
            $newToastIcon.addClass("fa-exclamation-circle");
            toastSeverity = "danger";
            break;
        default:  // Any other values.
            $newToastIcon.addClass("fa-question-circle");
            toastSeverity = "default";
            break;
    }

    $newToast.addClass("toast-" + toastSeverity);

    // Handle all animations.
    addToast($newToast);
    setTimeout(() => {removeToast($newToast)}, 5000);
}

// Make the animation appear with a fade-in effect.
let addToast = function($toastItem) {
    $toastItem.fadeIn(500);
}

// Remove the pop-up with a fade-out effect.
let removeToast = function($toastItem) {
    $toastItem.fadeOut(500, () => {
        $toastItem.remove()
    });
}

// Clicking on the button or pop-up content will close the pop-up.
$(document).on("click", ".toast > .toast-body > button", function(event) {
    event.preventDefault();
    removeToast($(this).parents(".toast"));
})
$(document).on("click", ".toast > .toast-body", function(event) {
    event.preventDefault();
    removeToast($(this).parents(".toast"));
})

$(document).ready(function() {
    $(".toast-template").hide()
})

// Add the notify function as a JQuery function, mainly to not break existing code.
$["notify"] = function(toastText, toastSeverity) {
    notify(toastText, toastSeverity);
};
