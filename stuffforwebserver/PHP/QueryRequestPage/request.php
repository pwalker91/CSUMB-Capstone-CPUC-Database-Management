<?PHP
//If the form has been submitted display the date chosen
if (isset($_POST['form_submit'])) {
    #Creating some of the nested arrays that will be passed in, and some other
    # generic criteria that needs to be in $_POST
    $toBeJSON = array( "file_criteria" => array(),
                       "test_criteria" => array());
    $toBeJSON['table'] = $_POST["form_ttype"];
    $testType = explode( "results", strtolower($_POST["form_ttype"]) );
    $testType = $testType[0];
    $toBeJSON['table_val'] = $_POST["form_ttype_".$testType."_val"];
    if ($_POST['form_ttype_group'] == "true") {
        $toBeJSON['grouping_test'] = "ConnectionLoc";
    }
    else {
        $toBeJSON['grouping_test'] = "";
    }
    $toBeJSON['grouping_file'] = $_POST["form_ftype_group"];

    #Now we want to remove the indeces we used, and the ones that we want to
    # avoid using when we are looping through the indeces.
    unset( $_POST["form_ttype"] );
    unset( $_POST["form_ttype_".$testType."_val"] );
    unset( $_POST["form_ttype_group"] );
    unset( $_POST["form_ftype_group"] );
    unset( $_POST["form_submit"] );
    #Removing the $_POST variables whose key contains "crit"
    foreach ($_POST as $key => $value) {
        if (strpos($key, "crit") !== False) {
            unset($_POST[$key]);
        }
    }

    #Now that we have an array with all of the elements we need, we want to
    # put the column names and values into our array
    foreach ($_POST as $key => $value) {
        if (strpos($key, "file") !== False) {
            $criteria = explode("form_file_", $key);
            $criteria = $criteria[1];
            $toBeJSON['file_criteria'][$criteria] = $_POST[$key];
        }
    }
    foreach ($_POST as $key => $value) {
        if (strpos($key, "ttype") !== False) {
            $criteria = explode("form_ttype_".$testType."_", $key);
            $criteria = $criteria[1];
            $toBeJSON['test_criteria'][$criteria] = $_POST[$key];
        }
    }

    #Now we make our JSON string. Our next step is to insert the information into
    # the database
    $theJSON = json_encode($toBeJSON);
    var_dump($theJSON);

    #Including our DB Connection info, and then insert into the database
    include('./_db_conn_default.php');
    $sql = "INSERT INTO PageRequest
            (`AnalysisOpts`,`ContactEmail`,`ContactName`)
            VALUES
            (:JSON, :email, :name)";
    $stmt = $db->prepare($sql);
    $stmt->execute( array (":JSON" => $theJSON,
                           ":email" => "",
                           ":name" => "") );
    $lastInsert = $db->lastInsertID();
    echo $lastInsert;
}

//Otherwise, echo the form
else {
    include("request_html.html");
}
?>
