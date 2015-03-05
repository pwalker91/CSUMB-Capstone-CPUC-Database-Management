
<html>
<body>
<form action="results.php" method="post">
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
   echo "<center>";
    $sql = "SELECT *
    FROM Overview
    WHERE 1";
    $result = $conn->query($sql);
    echo "choose a test result<br>";
    echo "<select name=id value='bob'>timmy</option>"; // list box select command
    
    

    
    if ($result->num_rows > 0) {
        // output data of each row
               while($row = $result->fetch_assoc()) {
           echo "<option value=$row[id]>$row[id]</option>";        }
        echo "<br>";
    } else {
        echo "0 results";
    }
   
    

?>
<br/>
<input type="submit"> </form>
</center>
</body>
</html>