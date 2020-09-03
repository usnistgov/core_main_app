/**
 * Change Data Display
 */
$(function(){
    $('#xslt-selector').change(function(){
        // get xsl transformation Id
        var xslt_id_param =  $("#xslt-selector").val()

        $.ajax({
            url: changeDataDisplayUrl,
            data: { "xslt_id": xslt_id_param,
                    "data_id": dataId
                  },
            dataType:"json",
            type: "post",
            success: function(data){
                $("#xslt-representation").html(data.template)
            },
            error: function(data){
                console.log(data)
            }
        });
    });
});
