/**
* Sharing button manager
*/

copyLink = function(link){
    /**
     * Copy the link on clipboard and close the modal
     */
    link.prop('disabled', false);
    link.focus();
    link.select();
    document.execCommand('copy');
    link.prop('disabled', true);
};

initSharingModal = function(sharingConfigurationFunction, sharingButtonId, sharingModalId,
                            sharingInputId, sharingSubmitId) {
    $(document).on('click', sharingButtonId, function(event) {
        event.preventDefault();
        let initialClasses = $(sharingButtonId+">i").attr("class");

        $(sharingButtonId+" i").removeClass();
        $(sharingButtonId+" i").addClass("fa fa-spinner fa-pulse");

        if (sharingConfigurationFunction()) {
            $(sharingModalId).modal("show");
        }

        $(sharingButtonId+" i").removeClass();
        $(sharingButtonId+" i").addClass(initialClasses);
    });
    $(document).on('click', sharingSubmitId, function(event) {
        event.preventDefault();
        copyLink($(sharingInputId));
        $(sharingModalId).modal("hide");
    });
};
