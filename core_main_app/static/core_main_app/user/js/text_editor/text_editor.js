let jqError = $('.alert-danger');
let documentID = null
let documentName = null
let templateID = null
let textEditorUrl = null
let showHTML = false
let useModal = false


/**
 * Load controllers for text editor
 */
$(document).ready(function() {
    documentID = $("#document_id").html()
    editorType = $("#editor_type").html()
    switch(editorType) {
        case "XSD":
            textEditorUrl = xsdTextEditorUrl
            break;

        default:
            templateID = $("#template_id").html();
            documentName = $("#document_name").html();
            if (documentName == "Data") textEditorUrl = dataXmlTextEditorUrl;
            else {
                textEditorUrl = draftXmlTextEditorUrl;
                $('.save-data').on('click', save);
                useModal = true;
            }
    }


    $('.btn.display').on('click', display);
    $('.btn.format').on('click', format);
    $('.btn.refresh').on('click', refresh);
    $('.btn.validate').on('click', validate);
    $('.btn.save').on('click', function(){
        if (useModal) createDataModal();
        else save();
    });


});

/**
 * AJAX, to save content
 */
let save = function()
{
   var icon = $(".save > i").attr("class");
   // Show loading spinner
   showSpinner($(".save > i"))
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
		     window.location =  data.url
	    },
        error:function(data){
            jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
            jqError.show();
        }
    }).always(function(data) {
        // get old button icon
        hideSpinner($(".save > i"), icon)
    });
   if (useModal) $("#create-data-modal").modal("hide");
};

/**
 * AJAX, to  format content
 */
let format = function()
{
   jqError.hide()
   var icon = $(".format > i").attr("class");
   // Show loading spinner
   showSpinner($(".format > i"))
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
    }).always(function(data) {
        // get old button icon
        hideSpinner($(".format > i"), icon)
    });
};

/**
 * AJAX, to validate content
 */
var validate = function()
{
     jqError.hide()
     var icon = $(".validate > i").attr("class");
     // Show loading spinner
     showSpinner($(".validate > i"))
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
	    },
        error:function(data){
           jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
           jqError.show();
        }
    }).always(function(data) {
        // get old button icon
        hideSpinner($(".validate > i"), icon)
    });

};

/**
 * AJAX, to refresh html content
 */
var refresh = function()
{
     var icon = $(".refresh > i").attr("class");
     // Show loading spinner
     showSpinner($(".refresh > i"))
     $.ajax({
            url: changeDataDisplayUrl,
            data: { "content": $(".input").text(),
                    "template_id": templateID,
                    "xslt_id": $("#xslt-selector").val()
                  },
            dataType:"json",
            type: "post",
            success: function(data){
                $.notify("Content refreshed with success", { style: "success" });
                $(".tree").html(data.template)

            },
            error: function(data){
                 jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
                 jqError.show();
            }
     }).always(function(data) {
        // get old button icon
        hideSpinner($(".refresh > i"), icon)
    });
};


/**
 * Show/Hide html representation
 */
let display = function(){
    var icon = $(".display > i").attr("class");
    // Show loading spinner
    showSpinner($(".display > i"))
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
    hideSpinner($(".display > i"), icon)
}


/**
* Shows a dialog to choose dialog options
*/
let createDataModal = function(){
  $("#create-data-modal").modal("show");
}