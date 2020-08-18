/** List detail xslt JS **/

$( document ).ready(function() {

   $(':checkbox').change(function() {

        var list_default_detail = $("#id_default_detail_xslt")
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
});
