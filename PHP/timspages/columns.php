
<html>
<body>
<form action="fuh.php" method="post">
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
    
    
    $sql = "SHOW COLUMNS FROM Overview";
    $result = mysqli_query($conn,$sql);
    while($row = mysqli_fetch_array($result)){
        $ROW1=$row['Field'];
        echo "<input type='radio' name='option' value='$ROW1'>";
        echo $row['Field']."<br>";
    }


    
    
    
    ?>
<input type=submit>
</form>
<br/>
</center>
</body>
</html>



#hidden input