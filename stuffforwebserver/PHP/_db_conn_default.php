<?php
$host = "localhost";
$username = "root";
$password = "cpuc";
$dbname = "cpuc";

//create connection
$db = new PDO("mysql:host=$host;dbname=$dbname;", $username, $password);

// Sets Error handling to Exception so it shows ALL errors when trying to get data
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

/*
$sql = 'SELECT * FROM table_name WHERE field_name = :field_name';
$stmt = $dbConn->prepare($sql);
$stmt->execute( array ( ":field_name" => "value");
$records_found = $stmt->fetchAll();

foreach ($records_found as $row) {
    echo $row['field1_name'];
}
*/
?>
