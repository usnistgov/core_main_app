let jqError = $('.alert-danger');
let documentID = null;
let documentName = null;
let templateID = null;
let textEditorUrl = null;
let showHTML = false;
let useModal = false;
let editorFormat = null;
let lineNumbers = 1;
let editor = null;
let widthInput = "45%";


/**
 * Load controllers for text editor
 */
$(document).ready(function() {
    documentID = $("#document_id").html();
    editorFormat = $("#editor_format").html();
    templateID = $("#template_id").html();
    documentName = $("#document_name").html();
    textEditor = $("#text_editor_library").html();

    if (textEditor == "Monaco"){
        value =  $("#data_content").text();
        editor = monaco.editor.create(document.getElementById('container'), {
            value: value,
            language: editorFormat.toLowerCase(),
            automaticLayout: true
        });
        widthInput = "50%";
    }
    else{
        // Synchronize line numbers with content
        $(".input").scroll(function() {
            $(".line-number").prop("scrollTop", this.scrollTop);
        });

        // Event to transform pasted content to plain text
        $('.input').on('paste', function(e) {
            e.preventDefault();
            // Get pasted text as plain text and set value into text editor
            setContent((e.originalEvent || e).clipboardData.getData('text/plain'));
        });
        // Synchronize line numbers  with the content
        refreshLineNumbers();
    }

    switch(editorFormat) {
        case "JSON":
            if (documentName == "Data") textEditorUrl = dataJSONTextEditorUrl;
            else {
                textEditorUrl = draftJSONTextEditorUrl;
                $("#switch-to-form" ).removeClass("hidden")
                $('.save-data').on('click', save);
                useModal = true;
            }
            break;
        case "XML":
            if (documentName == "Data") textEditorUrl = dataXmlTextEditorUrl;
            else {
                textEditorUrl = draftXMLTextEditorUrl;
                $("#switch-to-form" ).removeClass("hidden")
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
});

/**
 * Format a list of error message to output HTML ul/li list.
 *
 * @param errorList
 * @returns {string}
 */
function buildMessageFromList(errorList) {
    let node = document.createElement("ul");
    node.innerHTML = errorList.map((item) => {return `<li>${item}</li>`}).join("");

    // Display the list of item nicely.
    node.style.padding = "revert";
    node.style.margin = "0";
    node.style.listStyle = "initial";

    return node.outerHTML;
}

/**
 * Build an error message depending on the data passed.
 *
 * @param errorObject
 * @returns {string}
 */
function buildErrorMessage(errorObject) {
    if (typeof errorObject === "string") {
        return errorObject;
    } else if (Array.isArray(errorObject)) {
        return buildMessageFromList(errorObject);
    } else {
        return "Cannot display error: format not supported!";
    }
}

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
           'content': getContent(),
           'action': 'save',
           'document_id': documentID
        },
        dataType: "json",
		success: function(data){
		     window.location =  data.url
	    },
        error:function(data){
            let dataContent = null;
            try {
                dataContent = JSON.parse(data.responseText);
            } catch {
                dataContent = data.responseText;
            }
            jqError.html(
                `<i class="fas fa-exclamation-triangle"></i> An error occurred while saving: ${buildErrorMessage(dataContent)}`
            );
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
    if (textEditor == "Monaco" && editorFormat == "JSON"){
        editor.getAction('editor.action.formatDocument').run();
        $.notify("Document formatted successfully", "success");
    }
    else {
        jqError.hide();
        var icon = $(".format > i").attr("class");
        // Show loading spinner
        showSpinner($(".format > i"))
        $.ajax({
            url : textEditorUrl,
            type : "POST",
            data:{
                'content': getContent(),
                'action': 'format',
            },
            dataType: "json",
            success: function(data){
                $.notify("Document formatted successfully", "success");
                if(editorFormat == "JSON") data = JSON.stringify(data, null, "  ")
                setContent(data);
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
    }
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
           'content': getContent(),
           'action': 'validate',
           'template_id': templateID,
        },
        dataType: "json",
		success: function(data){
		   $.notify("Content validated with success", "success");
	    },
        error:function(data){
            let dataContent = null;
            try {
                dataContent = JSON.parse(data.responseText);
            } catch {
                dataContent = data.responseText;
            }
            jqError.html(
                `<i class="fas fa-exclamation-triangle"></i> An error occurred at validation: ${buildErrorMessage(dataContent)}`
            );
            jqError.show();
        }
    }).always(function(data) {
        // get old button icon
        hideSpinner($(".validate > i"), icon)
        refreshLineNumbers();
    });

};

/**
 * Refresh html content
 */
var refresh = function()
{
     updateDisplay($(".refresh > i"));
};

/**
 * AJAX, to update display
 */
var updateDisplay = function(iconSelector)
{
     var icon = iconSelector.attr("class");
     // Show loading spinner
     showSpinner(iconSelector)
     $.ajax({
            url: changeDataDisplayUrl,
            data: { "content": getContent(),
                    "template_id": templateID,
                    "xslt_id": $("#xslt-selector").val()
                  },
            dataType:"json",
            type: "post",
            success: function(data){
                $.notify("Display updated.", "success");
                $(".tree").html(data.template)

            },
            error: function(data){
                 jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ data.responseText);
                 jqError.show();
            }
     }).always(function(data) {
        // get old button icon
        hideSpinner(iconSelector, icon)
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
        updateDisplay($(".display > i"));
        $(".input").css("width", widthInput);
        $(".input").css("display", "inline-block");
        $(".display").html('<i class="fas fa-eye-slash"></i> Hide');
    }
    showHTML = !showHTML;
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
           'content': getContent(),
           'template_id': templateID,
           'action': 'generate',
        },
        dataType: "json",
		success: function(data){
		    $.notify("Document generated successfully", "success");
		    setContent(data);
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

let getContent = function(){
    if (textEditor == "Monaco")  return editor.getValue();
    else return $(".input").text();
}


let setContent = function(content){
    if (textEditor == "Monaco") editor.setValue(content);
    else {
        html = hljs.highlightAuto(content).value;
        $(".input").html("<pre class=\"content-highlight\">"+ html +"</pre>")
    }
}