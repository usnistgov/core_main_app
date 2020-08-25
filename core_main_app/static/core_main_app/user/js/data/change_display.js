/**
 * Change Data Display
 */
$(function(){
    $('#xslt-selector').change(function(){
        // get xsl transformation Id
        var xslt_id_param =  $("#xslt-selector").val()

        // get data Id
        data_id =  window.location.href.split("id=")[1]

        $.ajax({
            url: changeDataDisplayUrl,
            data: { "xslt_id": xslt_id_param,
                    "data_id": data_id
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
