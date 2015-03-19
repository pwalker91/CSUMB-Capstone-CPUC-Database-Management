if ($(document).ready( function() {
    $('.datePicker').datepicker({
        format: "yyyy-mm-dd",
        todayBtn: "linked",
        autoclose: true,
        todayHighlight: true
    });

    function resetSelect(selectTag) {
        $("#"+selectTag).val("...");
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



    function showError(elem){
        console.log("ERROR: No value in "+elem.name);
        $(elem).parents("div.form-group")
            .addClass("has-error");
        $(elem).parents("div.form-group").parent()
            .css('background-color', '#F0B2B2');
    }
    function removeError(elem){
        $(elem).parents("div.form-group")
            .removeClass("has-error")
        $(elem).parents("div.form-group").parent()
            .css('background-color', 'transparent');
    }

    $("#query_form").submit(function (){
        var ERRORSFOUND = false;
        $("#query_form input[type=radio]").each(function() {
            if(!$("input[name="+this.name+"]:checked").val()) {
                showError(this);
                ERRORSFOUND = true;
            }
            else {
                removeError(this);
            }
        });
        $("#query_form input[type=text]").each(function() {
            if(this.value=="") {
                showError(this);
                ERRORSFOUND = true;
            }
            else {
                removeError(this);
            }
        });
        $("#query_form input[type=date]").each(function() {
            if(this.value=="") {
                showError(this);
                ERRORSFOUND = true;
            }
            else {
                removeError(this);
            }
        });
        $("#query_form select").each(function() {
            if($(this).parent().css("display") != "none"){
                if(this.value=="") {
                    showError(this);
                    ERRORSFOUND = true;
                }
                else {
                    removeError(this);
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
                cache: false,
                success: function(json, status) {
                    console.log(status);
                    console.log(json);
                    var $description = $('<p>').text(json);
                    $('#info')
                        .empty()
                        .append($description);
                },
                error: function(xhr, desc, err) {
                    console.log(xhr);
                    console.log("Details: " + desc + "\nError:" + err);
                    var $errorMsg = $('<p>').text("Oops. Something went wrong...");
                    var $errorInfo = $('<p>').text("Details: " + desc + "\nError:" + err);
                    $('#info')
                        .empty()
                        .append($errorMsg)
                        .append($errorInfo);
                }
            });
        } /
    });*/
}));
