loadItemCount = function() {
    $("#admin-menu").find(".item_count").each(function(index, element) {
        var item_count_url = $(element).children("span").attr('id');

        $.ajax({
            url: item_count_url,
            method: "POST",
            success: function(data) {
                if (data.count !== 0) {
                    $(element).children("span").text(data.count);
                    $(element).children("span").removeClass('hidden');
                }
            }
        });
    });
};

$(document).ready(function () {
    loadItemCount();
});
