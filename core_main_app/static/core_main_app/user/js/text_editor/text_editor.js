let jqError = $('.alert-danger');
let documentID = null
let documentName = null
let templateID = null
let textEditorUrl = null
let showHTML = false


/**
 * Load controllers for text editor
 */
$(document).ready(function() {
    $('.btn.save').prop("disabled",true);
    documentID = $("#document_id").html()
    editorType = $("#editor_type").html()
    switch(editorType) {
        case "XSD":
            textEditorUrl = xsdTextEditorUrl
            break;

        default:
            templateID = $("#template_id").html();
            documentName = $("#document_name").html();
            if (documentName == "Data") textEditorUrl = dataXmlTextEditorUrl
            else textEditorUrl = draftXmlTextEditorUrl
    }


    $('.btn.display').on('click', display);
    $('.btn.format').on('click', format);
    $('.btn.refresh').on('click', refresh);
    $('.btn.save').on('click', save);
    $('.btn.validate').on('click', validate);



});

/**
 * AJAX, to save content
 */
let save = function()
{
   $.ajax({
        url : textEditorUrl,
        type : "POST",
        data:{
           'content': $(".input").text(),
           'action': 'save',
           'document_id': documentID
        },
        dataType: "json",
		success: function(data){
             if (documentName && documentName != "Data"){
                    window.location =  dataXmlTextEditorUrl+"?id="+data.data_id
             }
             else{
                  $.notify("Document saved with success", { style: "success" });
                  $('.btn.save').prop("disabled",true);
             }
	    },
        error:function(data){
            jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
            jqError.show();
        }
    });
};

/**
 * AJAX, to  format content
 */
let format = function()
{
   $('.btn.save').prop("disabled",true);
   jqError.hide()
   $.ajax({
        url : textEditorUrl,
        type : "POST",
        data:{
           'content': $(".input").text(),
           'action': 'format',
        },
        dataType: "json",
		success: function(data){
		    $.notify("Document formatted successfully", { style: "success" });
		    html = hljs.highlightAuto(data).value
		    $(".content-highlight").html(html)
	    },
        error:function(data){

            jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
            jqError.show();

        }
    });
};

/**
 * AJAX, to validate content
 */
var validate = function()
{
     jqError.hide()

     $.ajax({
        url : textEditorUrl,
        type : "POST",
        data:{
           'content': $(".input").text(),
           'action': 'validate',
           'template_id': templateID,
        },
        dataType: "json",
		success: function(data){
		   $.notify("Content validated with success", { style: "success" });
           $('.btn.save').prop("disabled",false);

	    },
        error:function(data){
           jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
           jqError.show();
        }
    });

};

/**
 * AJAX, to refresh html content
 */
var refresh = function()
{
     $.ajax({
            url: changeDataDisplayUrl,
            data: { "content": $(".input").text(),
                    "data_id": documentID,
                    "xslt_id": $("#xslt-selector").val()
                  },
            dataType:"json",
            type: "post",
            success: function(data){
                $(".tree").html(data.template)

            },
            error: function(data){
                 jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
                 jqError.show();
            }
     });
};


/**
 * Show/Hide html representation
 */
let display = function(){
    $(".representation").attr('hidden', showHTML)
    $(".refresh").attr('hidden', showHTML)
    $("#xslt-selector").attr('hidden', showHTML)
    if (showHTML){
       $(".input").css("width", "100%");
       $(".display").children().attr('class','fas fa-eye');
    }
    else{
        $(".input").css("width", "49%");
        $(".input").css("display", "inline-block");
        $(".display").children().attr('class','fas fa-eye-slash');

    }
    showHTML = !showHTML
}