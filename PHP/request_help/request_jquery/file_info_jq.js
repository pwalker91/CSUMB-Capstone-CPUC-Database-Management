/*
*   AUTHOR:     Peter Walker (pwalker@csumb.edu)
*   DATE:       21 March 2015
*   PURPOSE:    This file has a number of jQuery functions that are used when
*                creating input boxes for the user pertaining to their criteria
*                for specific files.
*/

if ($(document).ready( function() {

    //This is the AJAX function, used to determine if an HTML file exists. It uses
    // a callback function to modify the necessary HTML Element. Essentially, the AJAX
    // will execute, and once it's done, it will return a boolean the specified function.
    // It's that function that will modify the TABLE element.
    function urlExists(url, callback){
        $.ajax({
            type: 'HEAD',
            url: url,
            success: function(){
                callback(true);
            },
            error: function() {
                callback(false);
            }
        });
    }

    $('input[name="file_crit_button"]').click( function() {
        //Setting variables to hold the table we will be adding to, the value
        // of the select that the user selected, and the link to page we will
        // need (which has the form to append in it).
        var $table = $('table[name="file_criteria"]');
        var crit = $('select[name="form_file_crit"]').val();
        //If the user didn't pick nothing, then we continue
        if (crit) {
            if ($table.find("tr."+crit).length == 0 ) {
                var pageRoot = "http://54.200.224.217/csdi/request_help/request_criteria/"
                var pageLink = pageRoot+"file_"+crit+".html";
                //This block is because AJAX calls are asynchronous. What we have
                // to do is call this function (which uses the url given), and
                // have it perform another function after a callback. Basically,
                // the AJAX will execute, and will then say "hey, I have some data
                // for you to process.", and we want to handle that with our unnamed
                // function. If the page exists (callback was passed true), then we
                // add the table row
                urlExists(pageLink, function(exists){
                    if (exists){
                        $table
                        .append(
                            $("<tr>", { class: "field-start "+crit })
                            .append( $("<td>").load(pageLink) )
                            .append( $("<td>")
                                .addClass('field-remove')
                                .append($('<input>')
                                    .attr('type', 'button')
                                    .addClass('btn')
                                    .addClass('btn-danger')
                                    .addClass("remove-crit-button")
                                    .val("Remove")
                                    .click(function() {
                                        $(this).parents('tr.field-start').remove();
                                    })
                                )
                            )
                        )
                    }
                    else {
                        console.log("The page for the '"+crit+"' field does not exist.");
                    }
                });
            }
            else {
                console.log("The form already contains an input for the '"+crit+"' field.");
            }
        }
        else {
            console.log("No criteria field has been chosen.");
        }
    });
}));
