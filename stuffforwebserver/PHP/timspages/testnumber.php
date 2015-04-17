
<html>
<body>
<form action="results.php" method="post">
<?php
   
#Including our DB Connection info, and then insert into the database
    include('./_db_conn_default.php');



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
