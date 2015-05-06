<?php
if(isset($_GET['submit']))
{
  $host = "localhost";
  $username = "root";
  $password = "cpuc";
  $dbname = "cpuc";

  //create connection
  $db = new PDO("mysql:host=$host;dbname=$dbname;", $username, $password);
  // Sets Error handling to Exception so it shows ALL errors when trying to get data
  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  //Returns object to connect to
  $namedParameters = array();
	$sql="INSERT INTO `ContactPage` (`ContactName`, `ContactEmail`, `ErrorType`, `ErrorMessage`) VALUES (:name, :email, :error, :message)";
	$namedParameters[':name'] = $_GET['Name'];
	$namedParameters[':email'] = $_GET['email'];
	$namedParameters[':error'] = $_GET['subject'];
	$namedParameters[':message'] = $_GET['message'];
	$stmt = $dbConn -> prepare($sql);
 	$stmt -> execute($namedParameters);
}


?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">

		<!-- Always force latest IE rendering engine (even in intranet) & Chrome Frame
		Remove this if you use the .htaccess -->
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

		<title>new_file</title>
		<meta name="description" content="">
		<meta name="author" content="Nicholas Moradi">

		<meta name="viewport" content="width=device-width; initial-scale=1.0">

		<!-- Replace favicon.ico & apple-touch-icon.png in the root of your domain and delete these references -->
		<link rel="shortcut icon" href="/favicon.ico">
		<link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <meta http-equiv="refresh" content="0; url=csdi/contacts.php" />
	</head>

	<body>
		<div>
			<header>
				<h1>new_file</h1>
			</header>
			<nav>
				<p>
					<a href="/">Home</a>
				</p>
				<p>
					<a href="/contact">Contact</a>
				</p>
			</nav>

			<div>

			</div>

			<footer>
				<p>
					&copy; Copyright  by Nicholas Moradi
				</p>
			</footer>
		</div>
	</body>
</html>
