
<html>
<body>
<form action="fuh.php" method="post">
<?php
    ncluding our DB Connection info, and then insert into the database
    include('./_db_conn_default.php');


    
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
