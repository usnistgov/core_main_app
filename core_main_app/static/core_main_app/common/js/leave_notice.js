var leaveNotice = function(selector){
    jQuery(selector).filter(function() {
        return this.hostname && this.hostname !== location.hostname;
    }).click(function(e) {
       if(!confirm("You are about to proceed to an external website."))
       {
            // if user clicks 'no' then don't proceed to link.
            e.preventDefault();
       };
    });
}

jQuery(document).ready(leaveNotice('a'));