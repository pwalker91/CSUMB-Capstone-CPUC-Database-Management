/*
*   AUTHOR:     Peter Walker (pwalker@csumb.edu)
*   DATE:       21 March 2015
*   PURPOSE:    This file has a number of jQuery functions that are used when
*                creating input boxes for the user pertaining to their criteria
*                for the TCP tests that they want information from.
*/

if ($(document).ready( function() {
    //This function is for when a user is choosing a type of test
    // to have analysis done for, and hiding/showing the necessary DIVs.
    $('input[name="form_ttype"]:radio').change( function() {
        if ($(this).val()=="PINGResults") {
            //Appending all of the necessary options for this kind
            // of test to our Test Type Criteria section of the form
            $('div[name="form_ttype_val"]').empty()
                .append($('<select>')
                            .attr('name', 'form_ttype_ping_val')
                            .addClass('form-control')
                            .append( $('<option>').val('').text('- Please Choose a Value -') )
                            .append( $('<option>').val('RTTAverage').text('Delay') )
                            .append( $('<option>').val('PacketsLost').text('Packet Loss') )
                        )
                .append($('<span>')
                    .addClass("input-group-addon")
                    .addClass("add-on")
                    .append($('<span>')
                            .addClass("glyphicon")
                            .addClass("glyphicon-signal")
                            )
                );
            //Modifying the SELECT element in the 'Test Type Criteria' area to
            // have new options, specific to that type of test
            $('select[name="form_ttype_crit"]').empty()
                .append( $('<option>').val('').text('- Please Choose a Value -') )
                .append( $('<option>').val('ConnectionLoc').text('Connection Location') )
                .append( $('<option>').val('RTTMin').text('RTT Minimum') )
                .append( $('<option>').val('RTTMax').text('RTT Maximum') )
                .append( $('<option>').val('RTTAverage').text('RTT Average') )
                .append( $('<option>').val('RValue').text('R-Value') )
                .append( $('<option>').val('MOS').text('MOS Score') );
        }
        else if ($(this).val()=="UDPResults") {
            $('div[name="form_ttype_val"]').empty()
                .append($('<select>')
                            .attr('name', 'form_ttype_udp_val')
                            .addClass('form-control')
                            .append( $('<option>').val('').text('- Please Choose a Value -') )
                            .append( $('<option>').val('Jitter').text('Jitter') )
                            .append( $('<option>').val('Loss').text('Datagram Loss') )
                        )
                .append($('<span>')
                    .addClass("input-group-addon")
                    .addClass("add-on")
                    .append($('<span>')
                            .addClass("glyphicon")
                            .addClass("glyphicon-signal")
                            )
                );
            $('select[name="form_ttype_crit"]').empty()
                .append( $('<option>').val('').text('- Please Choose a Value -') )
                .append( $('<option>').val('ConnectionLoc').text('Connection Location') )
                .append( $('<option>').val('Jitter').text('Jitter Time') )
                .append( $('<option>').val('Loss').text('Percent Datagrams Lost') )
                .append( $('<option>').val('Time').text('Test Time Interval') );
        }
        else if ($(this).val()=="TCPResults") {
            $('div[name="form_ttype_val"]').empty()
                .append($('<select>')
                            .attr('name', 'form_ttype_tcp_val')
                            .addClass('form-control')
                            .append( $('<option>').val('').text('- Please Choose a Value -') )
                            .append( $('<option>').val('UpSpeed').text('Throughput - Upload Speed') )
                            .append( $('<option>').val('DownSpeed').text('Throughput - Download Speed') )
                        )
                .append($('<span>')
                    .addClass("input-group-addon")
                    .addClass("add-on")
                    .append($('<span>')
                            .addClass("glyphicon")
                            .addClass("glyphicon-signal")
                            )
                );
            $('select[name="form_ttype_crit"]').empty()
                .append( $('<option>').val('').text('- Please Choose a Value -') )
                .append( $('<option>').val('ConnectionLoc').text('Connection Location') )
                .append( $('<option>').val('UpSpeed').text('Upload Speed Average') )
                .append( $('<option>').val('UpStdDev').text('Upload Speed Standard Deviation') )
                .append( $('<option>').val('UpMedian').text('Upload Speed Median') )
                .append( $('<option>').val('UpPeriod').text('Upload Time Interval') )
                .append( $('<option>').val('UpPct').text('Active Uploading Percentage') )
                .append( $('<option>').val('DownSpeed').text('Download Speed Average') )
                .append( $('<option>').val('DownStdDev').text('Download Speed Standard Deviation') )
                .append( $('<option>').val('DownMedian').text('Download Speed Median') )
                .append( $('<option>').val('DownPeriod').text('Download Time Interval') )
                .append( $('<option>').val('DownPct').text('Active Downloading Percentage') );
        }
        else {
            $('#tcp_choices').hide();
            $('#udp_choices').hide();
            $('#ping_choices').hide();
            $('select[name="form_ttype_crit"]').empty();
        }
        //This clears the table of Test Type Criteria. If the user changes what
        // type of test they want, we need to remove any criteria they had made earlier
        $('table[name="ttype_criteria"]').html("");
    });


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

    $('input[name="ttype_crit_button"]').click( function() {
        //Setting variables to hold the table we will be adding to, the value
        // of the select that the user selected, and the link to page we will
        // need (which has the form to append in it).
        var $table = $('table[name="ttype_criteria"]');
        var crit = $('select[name="form_ttype_crit"]').val();
        var testType = $('input[name="form_ttype"]:radio:checked').val();
        //We only want to start checking if an html file exists if the user
        // has chosen a test type.
        if (testType) {
            testType = testType.toLowerCase().split("results")[0];
            //If the user didn't pick anything, then we continue
            if (crit) {
                if ($table.find("tr."+crit).length == 0 ) {
                    var pageRoot = "http://54.200.224.217/csdi/analysisRequest/request_criteria/"
                    var pageLink = pageRoot+testType+"_"+crit+".html";
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
                                    .append($('<input>')
                                        .attr('type', 'button')
                                        .addClass('btn')
                                        .addClass('btn-default')
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
                console.log("No criteria field has been chosen for the "+testType.toUpperCase()+" Test.");
            }
        }
        else {
            console.log("No test type has been chosen.")
        }
    });
}));
