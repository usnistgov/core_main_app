/**
 * Edit general information
 */
var modal = null;


editOpenModal = function(event) {
    event.preventDefault();
    var url = $(this).find('a').attr("href");

    $(modal).find('.modal-body').load(url, function () {
        $(modal).modal('show');
    });
};

editSave = function(event) {
    event.preventDefault();
    var form = $(modal).find('form');
    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: function (xhr, ajaxOptions, thrownError) {
            if ( $(xhr).find('.errorlist').length > 0 ) {
                $(modal).find('.modal-body').html(xhr);
                $(modal).trigger('error.bs.modal');
            } else {
                location.reload();;
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            if ( $(xhr).find('.errorlist').length > 0 ) {
                $(modal).find('.modal-body').html(xhr);
                $(modal).trigger('error.bs.modal');
            }
        }
    });
};

$(document).ready(function() {
    modal = $('#edit-object-modal');
    $('.edit').on('click', editOpenModal);
    $('#edit-object-save').on('click', editSave);
    $(modal).on('show.bs.modal error.bs.modal', function (e) {
        $(modal).find('form').on('submit', editSave);
    })
});
