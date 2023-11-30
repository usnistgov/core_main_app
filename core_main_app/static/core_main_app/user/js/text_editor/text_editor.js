let jqError = $('.alert-danger');
let documentID = null
let documentName = null
let templateID = null
let textEditorUrl = null
let showHTML = false
let useModal = false
let editorFormat = null
let lineNumbers = 1

/**
 * Load controllers for text editor
 */
$(document).ready(function() {
    documentID = $("#document_id").html()
    editorFormat = $("#editor_format").html()
    templateID = $("#template_id").html();
    documentName = $("#document_name").html();
    refreshLineNumbers()
    switch(editorFormat) {
        case "JSON":
            if (documentName == "Data") textEditorUrl = dataJSONTextEditorUrl;
            else {
                textEditorUrl = draftJSONTextEditorUrl;
                $('.save-data').on('click', save);
                useModal = true;
            }
            break;
        case "XML":
            if (documentName == "Data") textEditorUrl = dataXmlTextEditorUrl;
            else {
                textEditorUrl = draftXMLTextEditorUrl;
                $('.save-data').on('click', save);
                useModal = true;
            }
            break;
        case "XSD":
            textEditorUrl = xsdTextEditorUrl
            break;
    }


    $('.btn.display').on('click', display);
    $('.btn.format').on('click', format);
    $('.btn.refresh').on('click', refresh);
    $('.btn.validate').on('click', validate);
    $('.btn.generate').on('click', generate);
    $('.btn.save').on('click', function(){
        if (useModal) createDataModal();
        else save();
    });

    // Synchronize line numbers with content
    $(".input").scroll(function() {
        $(".line-number").prop("scrollTop", this.scrollTop);
    });

    // Event to transform pasted content to plain text
    $('.input').on('paste', function(e) {
        e.preventDefault();
        // Get pasted text as plain text
        var text = (e.originalEvent || e).clipboardData.getData('text/plain');
        // Highlight the text
        html = hljs.highlightAuto(text).value
        // Insert text into the editor input
        $(".input").html("<pre class=\"content-highlight\">"+ html +"</pre>")
        // Synchronize line numbers with the content pasted
        refreshLineNumbers();
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
        refreshLineNumbers();
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
		    $.notify("Document formatted successfully", "success");
		    if(editorFormat == "JSON") data = JSON.stringify(data, null, "  ")
		    html = hljs.highlightAuto(data).value
		    $(".input").html("<pre class=\"content-highlight\">"+ html +"</pre>")
	    },
        error:function(data){
            jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
            jqError.show();

        }
    }).always(function(data) {
        // get old button icon
        hideSpinner($(".format > i"), icon)
        refreshLineNumbers();
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
		   $.notify("Content validated with success", "success");
	    },
        error:function(data){
           jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
           jqError.show();
        }
    }).always(function(data) {
        // get old button icon
        hideSpinner($(".validate > i"), icon)
        refreshLineNumbers();
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
                $.notify("Content refreshed with success", "success");
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
    $(".representation").attr('hidden', showHTML)
    $(".refresh").attr('hidden', showHTML)
    $("#xslt-selector").attr('hidden', showHTML)
    if (showHTML){
        $(".input").css("width", "100%");
        $(".display").html('<i class="fas fa-eye"></i> Display');
    }
    else{
        $(".input").css("width", "45%");
        $(".test").css("width", "45%");
        $(".input").css("display", "inline-block");
        $(".display").html('<i class="fas fa-eye-slash"></i> Hide');
    }
    showHTML = !showHTML
}

/**
 * AJAX, to generate content
 */
let generate = function()
{
   jqError.hide()
   var icon = $(".generate > i").attr("class");
   // Show loading spinner
   showSpinner($(".generate > i"))
   $.ajax({
        url : textEditorUrl,
        type : "POST",
        data:{
           'content': $(".input").text(),
           'template_id': templateID,
           'action': 'generate',
        },
        dataType: "json",
		success: function(data){
		    $.notify("Document generated successfully", "success");
		    html = hljs.highlightAuto(data).value
		    $(".input").html("<pre class=\"content-highlight\">"+ html +"</pre>")
	    },
        error:function(data){
            jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
            jqError.show();

        }
    }).always(function(data) {
        // get old button icon
        hideSpinner($(".generate > i"), icon)
        // setup line numbers
        refreshLineNumbers();
    });
};



/**
* Shows a dialog to choose dialog options
*/
let createDataModal = function(){
  $("#create-data-modal").modal("show");
}


/**
* Refresh Line Numbers
*/
let refreshLineNumbers = function(){
    if( lineNumbers != $(".input").text().split('\n').length){
        var htmlLineNumber = ""
        lineNumbers = $(".input").text().split('\n').length
        for (i = 1;  i < lineNumbers + 1; i++){
            htmlLineNumber += "<span>"+i+"</span>"
        }
        $(".line-number").html(htmlLineNumber)
    }
}