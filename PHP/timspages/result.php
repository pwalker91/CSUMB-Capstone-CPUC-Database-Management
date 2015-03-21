<html>
<head>
<title>Results</title>
<?php
    $servername = "localhost";
    $username = "dyck5795";
    $password = "guest";
    $dbname = "dyck5795";
    
    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    ?>

</head>
<body>
<center>
<h1>results</h1>
<table border=1>
<tr>
<td rowspan="2">

<?php
    $sql = "SELECT *
    FROM Results
    WHERE PageHash=$_GET[d]
    ";
    $result = $conn->query($sql);
    while($row = $result->fetch_assoc()) {
        echo '<img src="http://hosting.otterlabs.org/classes/dycktimothya/cpuc/'.$row["ImagePath"]. '"/>';
    }
    echo "<br/><center><table border =1><script>";
    $result = $conn->query($sql);
    while($row = $result->fetch_assoc()) {
        echo $row["CalculatedData"];
    }
    
    echo ' var i=0
    while (i < 3){
        document.write(
                       "<tr><td>"+ employees[i].firstName + "</td><td>" + employees[i].lastName +"</td></tr>");
        i++;
    }
    
    </script></table></center';
    
    $conn->close();
    
    ?>
</td>
<td >
raw data<br/>
email yourself<br/>
help
</td>
</tr>
<tr>
<td>
related searches
</td>
</tr>
</table>
</center>
</body>
</html>