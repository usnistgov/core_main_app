/**
 * Delete general information
 */
var delete_modal = null;


deleteOpenModal = function(event) {
    event.preventDefault();
    var url = $(this).find('a').attr("href");

    $(delete_modal).find('.modal-body').load(url, function () {
        $(delete_modal).modal('show');
    });
};

deleteSave = function(event) {
    event.preventDefault();
    var form = $(delete_modal).find('form');
    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: function (xhr) {
            window.location.href = xhr.url;
        },
        error: function (xhr, ajaxOptions, thrownError) {
            $(delete_modal).find('.modal-body').html(xhr.responseText);
            $(delete_modal).trigger('error.bs.modal');
        }
    });
};

$(document).ready(function() {
    delete_modal = $('#delete-object-modal');
    $('.delete').on('click', deleteOpenModal);
    $('#delete-object-save').on('click', deleteSave);
    $(delete_modal).on('show.bs.modal error.bs.modal', function (e) {
        $(delete_modal).find('form').on('submit', deleteSave);
    })
});
