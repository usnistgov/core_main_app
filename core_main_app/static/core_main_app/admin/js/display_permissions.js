/** Django admin permissions JS **/


/**
 * Init controllers for the django admin permissions page
 */

document.addEventListener('DOMContentLoaded', function() {

        // Mouse enter event handler for the 'option' elements inside 'select'
        document.addEventListener('mouseover', function(event) {
            if (event.target.tagName === 'OPTION') {
                // Move permission's label left
                if (event.target.scrollWidth > event.target.clientWidth + 8) {
                    // get overflow value
                    let overflow = event.target.scrollWidth - event.target.clientWidth - 8;
                    // get missing text percentage
                    let textIndentPercentage = (overflow * 100) / (event.target.clientWidth - 8);
                    event.target.style.textIndent = -textIndentPercentage + "%";
                }
            }
        });

        // Mouse leave event handler for the 'option' elements inside 'select'
        document.addEventListener('mouseout', function(event) {
            if (event.target.tagName === 'OPTION') {
                // Move permission's label right
                event.target.style.textIndent = "0%";
            }
        });

});




