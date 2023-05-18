var row;

function start(){  
  row = event.target;
}

function dragover(){
  var e = event;
  e.preventDefault();
  let children= Array.from(e.target.parentNode.parentNode.children);
  
  if(children.indexOf(e.target.parentNode)>children.indexOf(row))
    e.target.parentNode.after(row);
  else
    e.target.parentNode.before(row);

  // disable save ordering button
  $(".save-order").prop("disabled",false);
  $(".save-order-global").prop("disabled",false);
}


/**
 * AJAX, to save template ordering
 */
var saveTemplateOrdering = function(event, url)
{
   // get template ids
   let queryData = {}
   queryData.template_list = $("tr[object-id]").map(function() {
        return ($(this).attr("object-id"));
   }).get();

   $.ajax({
        url : url,
        type: "patch",
        contentType: "application/json",
        data: JSON.stringify(queryData),
        dataType: 'json',
        success : function(data) {
             location.reload();
             $(".save-order").prop("disabled",true);
             $(".save-order-global").prop("disabled",true);
        },
        error: function(data){
            $(".error-container").show();
            $("#error-text").html("Impossible to change template order: "+ data.responseText);
        }
    });
};

$(document).ready(function() {
    $('.save-order').on('click', e=>saveTemplateOrdering(e, saveUserTemplateOrderingUrl));
    $('.save-order-global').on('click', e=>saveTemplateOrdering(e, saveGlobalTemplateOrderingUrl));
});
