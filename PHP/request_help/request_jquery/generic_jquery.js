/*
*   AUTHOR:     Peter Walker (pwalker@csumb.edu)
*   DATE:       18 March 2015
*   PURPOSE:    This file has a number of jQuery functions that are used in different
*                places within the request.php page, but mostly are for either
*                showing or hiding elements.
*/


if ($(document).ready( function() {
    //For showing or removing an error from the form. This will add
    // the 'has-error' class to the parent div that is a 'form-elem' class, and
    // to the parent div that is of 'input-col' class.
    // It will also change the background of the parent 'field-start' div
    // to have a red background
    function showError(elem){
        console.log("ERROR: No value in "+elem.name);
        $(elem).parents("div.input-col")
            .addClass("has-error");
        var $form_elem = $(elem).parents("div.form-elem");
        $($form_elem)
            .addClass("has-error");
        $($form_elem).parents('.field-start')
            .css('background-color', '#F0B2B2');
    }
    //This is the opposite of show error. It removed the red background color,
    // and removes the 'has-error' class.
    // However, this removing is only done to the 'form-elem' and 'field-start'
    // elements if no other child elements in the 'form-elem' have errors.
    function removeError(elem){
        $(elem).parents("div.input-col")
            .removeClass("has-error");
        var $form_elem = $(elem).parents("div.form-elem");
        var noErrors = true;
        $($form_elem).children('div.input-col').each(function() {
            if ($(this).hasClass("has-error")) {
                noErrors = false;
            }
        });
        if (noErrors) {
            $($form_elem)
                .removeClass("has-error");
            $($form_elem).parents('.field-start')
                .css('background-color', 'transparent');
        }
    }



    //When the query form is submitted, we need to check that all of the inputs
    // have been filled out.
    // We are going to check every type of input currently used that has
    // a 'form-elem' class. If an error is found, we show that error with showError(),
    // and set ERRORSFOUND to true. We will then return the NOT of that boolean once
    // we complete
    $("#query_form").submit(function (){
        var ERRORSFOUND = false;
        //Checking that a radio button has been checked
        $("#query_form input[type=radio]").each(function() {
            if ($(this).parents("div.form-elem").length > 0) {
                if (!$("input[name="+this.name+"]:checked").val()) {
                    showError(this);
                    ERRORSFOUND = true;
                }
                else {
                    removeError(this);
                }
            }
        });
        //Checking that a text input has been filled in
        $("#query_form input[type=text]").each(function() {
            if ($(this).parents("div.form-elem").length > 0) {
                if ($(this).val()=="") {
                    showError(this);
                    ERRORSFOUND = true;
                }
                else {
                    removeError(this);
                }
            }
        });
        //Checking that a date input has been filled in
        $("#query_form input[type=date]").each(function() {
            if ($(this).parents("div.form-elem").length > 0) {
                if ($(this).val()=="") {
                    showError(this);
                    ERRORSFOUND = true;
                }
                else {
                    removeError(this);
                }
            }
        });
        //Checking that a select option has been chosen
        $("#query_form select").each(function() {
            if ($(this).parents("div.form-elem").length > 0) {
                if ($(this).parent().css("display") != "none"){
                    if($(this).val()=="") {
                        showError(this);
                        ERRORSFOUND = true;
                    }
                    else {
                        removeError(this);
                    }
                }
            }
        });
        return !ERRORSFOUND;
    });
}));
