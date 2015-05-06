<html>
<head>
<style>
	body 
	{
   		 background-image: url('images/wireless-tower.jpg');
    		 background-repeat: no-repeat;
   		 background-attachment: fixed;
   		 background-position: 72% 66%;
	}


	h1 
	{
    	color: #000000;
    	margin-left: 40px;
    	text-shadow: 2px 2px #58B9ED;
	} 
	table, th, td 
	{
   		border: 1px solid black;
	} 
</style>
<title>Results</title>
<?php
    $servername = "localhost";
    $username = "root";
    $password = "cpuc";
    $dbname = "cpuc";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    ?>

</head>
<center>
<body>
<h1>Sample CalSPEED Imaging Data Results</h1>

<?php
    $sql = "SELECT *
    FROM PageResults
    WHERE PageHash=\"$_GET[d]\"
    ";
    $result = $conn->query($sql);
    while($row = $result->fetch_assoc()) {
    $var=substr_replace($row["ImagePath"] ,"",0,59);
    echo '<table><img src="./images' .$var. '" style="width:304px;height:228px";/></table>';


        $json = json_decode($row["CalculatedData"]);
       // echo json_encode($json);
       // echo "<br>";
        $moo = json_decode($row["MetaInfo"]);
        //echo "<br>";
        //echo json_encode($moo);


        }
      
    echo "<br />";

//echo json_encode($moo);
    //echo "<table border=1>";
    foreach($moo->columnNames as $item){
        echo "<tr>";
        echo "<table bgcolor = #FFFFFF align=left>";
        echo "<td>";
        echo $item;
        foreach($json->$item as $test){
            echo "<td>" . $test;
        }
        echo "</td></td></table></tr>";	
    }


    ?>
</td>
</tr>


   </table>
<table>
<td>
raw data<br/>
<?php
echo json_encode($moo);
 $conn->close();
    ?>
</td>
</tr>
<tr>
<td>
<a href="../home.php">Home</a><br/>
<a href="../contacts.php">Help</a><br/>
<a href="../analysisRequest/request.php" >Related Searches</a>
</td>
</tr>
</table>
</body>
</center>
</html>
