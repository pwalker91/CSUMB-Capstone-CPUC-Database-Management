<?
//If the form has been submitted display the date chosen
if (isset($_POST['form_submit'])) {
    $s = json_encode($_POST);
    echo $s;
}

//Otherwise, echo the form
else {
    include("request_html.html");
}
?>
