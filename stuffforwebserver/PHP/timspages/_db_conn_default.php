<?php
$host = "localhost";
$username = "root";
$password = "cpuc";
$dbname = "cpuc";

//create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Sets Error handling to Exception so it shows ALL errors when trying to get data
#$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

#echo "fish!!!!!";

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
