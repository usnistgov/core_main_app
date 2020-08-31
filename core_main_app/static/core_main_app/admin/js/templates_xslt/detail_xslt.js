/** List detail xslt JS **/

$( document ).ready(function() {

	// activate all the tooltips of the page
    $('[data-toggle="tooltip"]').tooltip()

   $(':checkbox').change(function() {

        var list_default_detail = $("#id_default_detail_xslt");
        var id_xslt = $(this).val();
        var isChecked = $(this).prop('checked');

        var name_xslt =  $("label[for="+this.id+"]").text();

         if(isChecked == true){
            // Add the checked option to default detail list
            list_default_detail.append($("<option></option>").attr("value", id_xslt).text(name_xslt));
         }
         else {
            // Remove the checked option from default detail list
            $("#id_default_detail_xslt option[value="+id_xslt+"]").remove();
         }
    });

    initDefaultDropdown();
});

let initDefaultDropdown = () => {
    let list_default_detail = $("#id_default_detail_xslt");
    let jqDefaultSelect = $("select[name=default_detail_xslt]");
    let selectValue = jqDefaultSelect[0].value;

    // reset the select content
    jqDefaultSelect.html('<option value="">(No XSLT)</option>')

    let jqCheckedInput = $("input[name]:checked").each( (index, item) => {
        let labelText = item.parentElement.textContent;
        list_default_detail.append($("<option></option>").attr("value", item.value).text(labelText));
    } );

    // if the for has a preset value
    if(selectValue) {
        jqDefaultSelect[0].value = selectValue;
    }
}
