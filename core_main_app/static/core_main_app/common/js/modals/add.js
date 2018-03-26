/**
 * Add general information
 */
var add_modal = null;


addOpenModal = function(event) {
    event.preventDefault();
    var url = $(this).find('a').attr("href");

    $(add_modal).find('.modal-body').load(url, function () {
        $(add_modal).modal('show');
    });
};

addSave = function(event) {
    event.preventDefault();
    var form = $(add_modal).find('form');
    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: function (xhr) {
            if(xhr.is_valid){
                window.location.href = xhr.url;
            }
            else {
                $(add_modal).find('.modal-body').html(xhr.responseText);
                $(add_modal).trigger('error.bs.modal');
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            $(add_modal).find('.modal-body').html(xhr.responseText);
            $(add_modal).trigger('error.bs.modal');
        }
    });
};

$(document).ready(function() {
    add_modal = $('#add-object-modal');
    $('.add').on('click', addOpenModal);
    $('#add-object-save').on('click', addSave);
    $(add_modal).on('show.bs.modal error.bs.modal', function (e) {
        $(add_modal).find('form').on('submit', addSave);
    })
});
