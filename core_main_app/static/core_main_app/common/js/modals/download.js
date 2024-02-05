/**
 * AJAX call, download document
 * @param document
 */
download = function(e){
    let toFormat = $('#format').is(':checked')
    let downloadUrl;
    if (e.data.document == "document") downloadUrl = downloadDocumentUrl
    else downloadUrl = downloadTemplateUrl
    window.location.href = downloadUrl +"?pretty_print=" + toFormat;

};


$('.download-document-btn').on('click', {document: 'document'}, download);
$('.download-template-btn').on('click', {document: 'template'}, download);