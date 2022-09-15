/** Django admin permissions JS **/


/**
 * Init controllers for the django admin permissions page
 */
$(document).ready(function() {
     $('select').on('mouseenter','option',displayFromRightToLeft);
     $('select').on('mouseleave','option',displayFromLeftToRight);
});

/**
 * Move permission's label right
 */
var displayFromLeftToRight = function(e){
    $(this).css("text-indent","0%");
}

/**
 * Move permission's label left
 */
var displayFromRightToLeft = function(e){
      if($(this)[0].scrollWidth>$(this).width()+8){
            // get overflow value
            let overflow = $(this)[0].scrollWidth - $(this).width() - 8
            // get missing text percentage
            let textIndentPercentage = overflow*100/($(this).width() - 8)
            $(this).css("text-indent",-textIndentPercentage+"%");
      }
}

