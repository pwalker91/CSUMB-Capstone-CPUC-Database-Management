<?php
$host = "localhost";
//this changes from user to user
$dbname ="mora3237";
//
$username = "mora3237";
//
$password = "secret";
//establishes connection to the MySQL database
$dbConn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
$dbConn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
//used to establish which table the we will be querying specifically
//just incase its too hard to ask user to select table
//but that shouldn't be hard
$sql = "USE TABLE Overview";
$stmt = $dbConn -> prepare($sql);
$stmt -> execute ();
$result = $stmt -> fetchAll();

?>
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<title>Work In Progress.</title>
</head>

<body>
	<form>
		Carriers:
		<br />
		<select>
			<option>All</option>
			<option>Verizon</option>
			<option>T-Mobile</option>
			<option>Sprint</option>
			<option>AT&T</option>

		</select>
		Location:
		<br />
		<select>
			<option>Both</option>
			<option>West</option>
			<option>East</option>

		</select>
		Type of Connection:
		<br />
		<select>
			<option>All</option>
			<option>UDP</option>
			<option>TCP</option>

		</select>
		Connection Speeds:
		<select>
			<option>All</option>
			<option>DownSpeed</option>
			<option>UpSpeed</option>
		</select>
		Statistics:
		<select>
			<option>None</option>
			<option>Mean</option>
			<option>Median</option>
			<option>Max</option>
		</select>
	</form>
</body>
</html>
