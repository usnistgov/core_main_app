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

initSharingModal = function(sharingData, sharingButtonId, sharingModalId,
                            sharingInputId, sharingSubmitId) {
    $(sharingInputId).val(sharingData);

    $(document).on('click', sharingButtonId, function(event) {
        event.preventDefault();
        $(sharingModalId).modal("show");
    });
    $(document).on('click', sharingSubmitId, function(event) {
        event.preventDefault();
        copyLink($(sharingInputId));
        $(sharingModalId).modal("hide");
    });
};
