<html>
<head>
    <meta charset="utf-8">
    <title>Choose a File by DATE</title>
    <style>
        table, tr
            {   border:1px solid black;
                background-color:#80CCFF;
            }
        td
            {   background-color:#FF8282;
            }
        th
            {   background-color:#FFFF99
            }
    </style>

    <link rel="stylesheet" href="http://code.jquery.com/ui/1.11.3/themes/smoothness/jquery-ui.css">
    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <script>
        $(function() {
            //Our date picker that will pass the date selected
            // to the AJAX function
            $( "#datepicker" ).datepicker({
                onSelect: function() {
                    var date = $(this).val().split("/");
                    var newDate = date[2]+"-"+date[0]+"-"+date[1];
                    //alert( newDate );

                    $.ajax({
                        url: './_queryInfo.php',
                        type: "post",
                        data: {
                            'date': newDate
                        },
                        cache: false,
                        success: function(json, status) {
                            console.log(status);
                            console.log(json);
                            //var $title = $('<h1>').text(data.talks[0].talk_title);
                            var $description = $('<p>').text(json);
                            $('#info')
                                .empty()
                                .append($description);
                        },
                        error: function(xhr, desc, err) {
                            console.log(xhr);
                            console.log("Details: " + desc + "\nError:" + err);
                            var $errorInfo = $('<p>').text("Oops. Something went wrong...")
                            $('#info')
                                .empty()
                                .append($errorInfo);
                        }
                    });
                }
            });
        });
    </script>
</head>

<body>
    <div id="selection" style="text-align:center;">
        <h2>Please choose a date. This will query for all tests conducted on that day</h2>
        <p>
            <b>The current possible date ranges are...</b><br>
            05/26/2014 - 05/30/2014<br>
            11/03/2014 - 11/07/2014
            </ul>
        </p>
        <p>Date: <input type="text" id="datepicker"></p>
    </div>

    <div id="info"></div>
</body>
</html>



<?PHP
/*



SCRIPT
$('#action-button').click(function() {
   $.ajax({
      url: 'http://api.joind.in/v2.1/talks/10889',
      data: {
         format: 'json'
      },
      error: function() {
         $('#info').html('<p>An error has occurred</p>');
      },
      dataType: 'jsonp',
      success: function(data) {
         var $title = $('<h1>').text(data.talks[0].talk_title);
         var $description = $('<p>').text(data.talks[0].talk_description);
         $('#info')
            .append($title)
            .append($description);
      },
      type: 'GET'
   });
});





PHP
$arr = array('a' => 1, 'b' => 2, 'c' => 3, 'd' => 4, 'e' => 5);
echo json_encode($arr);

PHP
$json = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
var_dump(json_decode($json));
var_dump(json_decode($json, true));

NULL returned if JSON cannot be decoded





if (isset($_POST['create_submit']))
{
    include('/home/CLASSES/walkerpeterj/CST336/.db_conn_default.php');

    $query = "INSERT INTO 336_IP_users (first_name, last_name, username, password, pass_hint, email) "
            ."VALUES "
            ."(:first_name, :last_name, :username, :password, :hint, :email)";
    $values = array( ":first_name" => $_POST['first_name'],
                     ":last_name" => $_POST['last_name'],
                     ":username" => $_POST['username'],
                     ":password" => hash("whirlpool", $_POST['password']),
                     ":hint" => $_POST['pass_hint'],
                     ":email" => $_POST['email'] );

    $handle = $db->prepare($query);
    $handle->execute($values);

    unset($_POST['create_submit']);
    $db = null;
    $_SESSION['login_error'] = 'false';
}*/
?>
