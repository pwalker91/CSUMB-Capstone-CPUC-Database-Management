<html>
<head>
<title>Contacts</title>

</head>
<body>

<h1>tcp results</h1>
<?php
   
#Including our DB Connection info, and then insert into the database
    include('./_db_conn_default.php');



 
    $sql = "SELECT *
    FROM Overview
    JOIN PINGResult
    ON Overview.id=PINGResult.oid
    JOIN TCPResult
    ON TCPResult.oid=Overview.id
    JOIN UDPResult
    ON UDPResult.oid=Overview.id
    WHERE 1";
    $result = $conn->query($sql);
    
    if ($result->num_rows > 0) {
        // output data of each row
        echo "<table border=1><tr><td>id</td><td>Timestamp</td><td>OSName_OSArchitecture_OSVersion</td><td>JavaVersion_JavaVendor</td><td>DeviceID</td><td>DeviceType</td><td>Server</td><td>Host</td><td>NetworkCarrier</td><td>NetworkProvider</td><td>NetworkOperator</td><td>ConnectionType</td><td>LocationID</td><td>Tester</td><td>Date</td><td>Time</td><td>Latitude</td><td>Longitude</td><td>AvgLatitude</td><td>AvgLongitude</td><td>ErrorType</td><td>FileLocation</td><td>Flag</td><td>FlagMessage</td><td>ConnectionLoc</td><td>TestNumber</td><td>WindowSize</td><td>Port</td><td>UpSpeed</td><td>UpStdDev</td><td>UpMedian</td><td>UpPeriod</td><td>UpPct</td><td>DownSpeed</td><td>DownStdDev</td><td>DownMedian</td><td>DownPeriod</td><td>DownPct</td><td>ErrorType</td></tr>";
        while($row = $result->fetch_assoc()) {
            echo "<tr><td>".$row["id"]."</td><td>".$row["Timestamp"]."</td><td>".$row["OSName_OSArchitecture_OSVersion"]."</td><td>".$row["JavaVersion_JavaVendor"]."</td><td>".$row["DeviceID"]."</td><td>".$row["DeviceType"]."</td><td>".$row["Server"]."</td><td>".$row["Host"]."</td><td>".$row["NetworkCarrier"]."</td><td>".$row["NetworkProvider"]."</td><td>".$row["NetworkOperator"]."</td><td>".$row["ConnectionType"]."</td><td>".$row["LocationID"]."</td><td>".$row["Tester"]."</td><td>".$row["Date"]."</td><td>".$row["Time"]."</td><td>".$row["Latitude"]."</td><td>".$row["Longitude"]."</td><td>".$row["AvgLatitude"]."</td><td>".$row["AvgLongitude"]."</td><td>".$row["ErrorType"]."</td><td>".$row["FileLocation"]."</td><td>".$row["Flag"]."</td><td>".$row["FlagMessage"]."</td><td>".$row["ConnectionLoc"]."</td><td>".$row["TestNumber"]."</td><td>".$row["WindowSize"]."</td><td>".$row["Port"]."</td><td>".$row["UpSpeed"]."</td><td>".$row["UpStdDev"]."</td><td>".$row["UpMedian"]."</td><td>".$row["UpPeriod"]."</td><td>".$row["UpPct"]."</td><td>".$row["DownSpeed"]."</td><td>".$row["DownStdDev"]."</td><td>".$row["DownMedian"]."</td><td>".$row["DownPeriod"]."</td><td>".$row["DownPct"]."</td><td>".$row["ErrorType"]."</td></tr>";
        }
        echo "</table>";
    } else {
        echo "0 results";
    }
    $conn->close();
    ?>


</body>
</html>
