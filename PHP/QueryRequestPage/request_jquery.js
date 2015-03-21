if ($(document).ready( function() {
    $('.datePicker').datepicker({
        format: "yyyy-mm-dd",
        todayBtn: "linked",
        autoclose: true,
        todayHighlight: true
    });

    function resetSelect(selectTag) {
        $("#"+selectTag).val("");
    }
    function showPNG() {
        $('#tcp_choices').hide();
        resetSelect('tcp_choices');
        $('#udp_choices').hide();
        resetSelect('udp_choices');
        $('#ping_choices').show();
    }
    function showUDP() {
        $('#tcp_choices').hide();
        resetSelect('tcp_choices');
        $('#udp_choices').show();
        $('#ping_choices').hide();
        resetSelect('ping_choices');
    }
    function showTCP() {
        $('#tcp_choices').show();
        $('#udp_choices').hide();
        resetSelect('udp_choices');
        $('#ping_choices').hide();
        resetSelect('ping_choices');
    }

    $('input[name="form_ttype"]:radio').change( function() {
        if ($(this).val()=="PING") { showPNG(); }
        else if ($(this).val()=="UDP") { showUDP(); }
        else if ($(this).val()=="TCP") { showTCP(); }
    });



    //For adding rows to either the File criteria, or the Test Type criteria
    $('input[name="show_date_div"]').click( function() {
        $('table[name="file_criteria"]').append(
            $("<tr>", {
                class: "field-start"
            }).append(
                $("<td>").load("request_criteria/file_date.html")
            )
        );
    });

    $('input[name="show_loc_div"]').click( function() {
        $('table[name="test_type_criteria"]').append(
            $("<tr>", {
                class: "field-start"
            }).append(
                $("<td>").load("request_criteria/tcp_loc.html")
            )
        );
    });



    //For showing or removing an error from the form
    function showError(elem){
        console.log("ERROR: No value in "+elem.name);
        var input_col = $(elem).parents("div.input-col");
        $(input_col)
            .addClass("has-error");
        var form_grp = $(input_col).parents("div.form-elem");
        $(form_grp)
            .addClass("has-error");
        $(form_grp).parents('.field-start')
            .css('background-color', '#F0B2B2');
    }
    function removeError(elem){
        var input_col = $(elem).parents("div.input-col")
        $(input_col)
            .removeClass("has-error");
        var form_grp = $(input_col).parents("div.form-elem");
        var noErrors = true;
        $(form_grp).children('div.input-col').each(function() {
            if ($(this).hasClass("has-error")) {
                noErrors = false;
            }
        });
        if (noErrors) {
            $(form_grp)
                .removeClass("has-error");
            $(form_grp).parents('.field-start')
                .css('background-color', 'transparent');
        }
    }

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

    // AJAX
    /*
    //Our date picker that will pass the date selected
    // to the AJAX function
    $( ".datepicker" ).datepicker({

        format: "yyyy-mm-dd",
        todayBtn: "linked",
        autoclose: true,
        todayHighlight: true

        /*
        onSelect: function() {
            var date = $(this).val().split("/");
            var newDate = date[2]+"-"+date[0]+"-"+date[1];
            $.ajax({
                url: 'http://hosting.otterlabs.org/classes/walkerpeterj/CSDI/_queryInfo.php',
                type: "post", //"get"
                data: {
                    'date': newDate //,
                    //'elem2': val2
                },
      