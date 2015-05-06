<html>
<head>
<title>Sampled Results</title>

</head>
<body>
  <h1>overview </h1>
<?php

      $sel=$_POST["id"];
      $sql = "SELECT * FROM FileInfo";
      $result = $conn->query($sql);

      if ($result->num_rows > 0) {
          // output data of each row
          echo "<table border=1><tr><td>id</td><td>Timestamp</td><td>OSName_OSArchitecture_OSVersion</td><td>JavaVersion_JavaVendor</td><td>DeviceID</td><td>DeviceType</td><td>Server</td><td>Host</td><td>NetworkCarrier</td><td>NetworkProvider</td><td>NetworkOperator</td><td>ConnectionType</td><td>LocationID</td><td>Tester</td><td>Date</td><td>Time</td><td>Latitude</td><td>Longitude</td><td>AvgLatitude</td><td>AvgLongitude</td><td>ErrorType</td><td>FileLocation</td><td>Flag</td><td>FlagMessage</td></tr>";
          while($row = $result->fetch_assoc()) {
              echo "<tr><td>".$row["Id"]."</td><td>".$row["InsertTimestamp"]."</td><td>".$row["OSName"]."</td><td>".$row["JavaVendor"]."</td><td>".$row["DeviceID"]."</td><td>".$row["DeviceType"]."</td><td>".$row["Server"]."</td><td>".$row["Host"]."</td><td>".$row["NetworkCarrier"]."</td><td>".$row["NetworkProvider"]."</td><td>".$row["NetworkOperator"]."</td><td>".$row["ConnectionType"]."</td><td>".$row["LocationID"]."</td><td>".$row["Tester"]."</td><td>".$row["Date"]."</td><td>".$row["Time"]."</td><td>".$row["Latitude"]."</td><td>".$row["Longitude"]."</td><td>".$row["AvgLatitude"]."</td><td>".$row["AvgLongitude"]."</td><td>".$row["ErrorType"]."</td><td>".$row["FileLocation"]."</td><td>".$row["Flag"]."</td><td>".$row["FlagMessage"]."</td></tr>";
          }
          echo "</table>";
      } else {
          echo "no data available";
      }



    echo "<h1>PING Results </h1>";

    $sql = "SELECT * FROM PINGResults";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // output data of each row
        echo "<table border=1><tr><td>ConnectionLoc</td><td>TestNumber</td><td>PacketsSent</td><td>PacketsReceived</td><td>PacketsLost</td><td>RTTMin</td><td>RTTMax</td><td>RTTAverage</td><td>RValue</td><td>MOS</td><td>ErrorType</td></tr>";
        while($row = $result->fetch_assoc()) {
          echo "<tr><td>".$row["ConnectionLoc"]."</td><td>".$row["TestNumber"]."</td><td>".$row["PacketsSent"]."</td><td>".$row["PacketsReceived"]."</td><td>".$row["PacketsLost"]."</td><td>".$row["RTTMin"]."</td><td>".$row["RTTMax"]."</td><td>".$row["RTTAverage"]."</td><td>".$row["RValue"]."</td><td>".$row["MOS"]."</td><td>".$row["ErrorType"]."</td></tr>";

        }
        echo "</table>";
    } else {
        echo "no data available";
    }

     echo "<h1>TCP Results</h1>";

     $sql = "SELECT * FROM TCPResults";
     $result = $conn->query($sql);

     if ($result->num_rows > 0)
     {
         // output data of each row
         for($i = 0; $i < 10; $i++)
         echo "<table border=1><tr><td>ConnectionLoc</td><td>TestNumber</td><td>WindowSize</td><td>Port</td><td>UpSpeed</td><td>UpStdDev</td><td>UpMedian</td><td>UpPeriod</td><td>UpPct</td><td>DownSpeed</td><td>DownStdDev</td><td>DownMedian</td><td>DownPeriod</td><td>DownPct</td><td>ErrorType</td></tr>";
         while($row = $result->fetch_assoc())
         {
             echo "<tr><td>".$row["ConnectionLoc"]."</td><td>".$row["TestNumber"]."</td><td>".$row["WindowSize"]."</td><td>".$row["Port"]."</td><td>".$row["UpSpeed"]."</td><td>".$row["UpStdDev"]."</td><td>".$row["UpMedian"]."</td><td>".$row["UpPeriod"]."</td><td>".$row["UpPct"]."</td><td>".$row["DownSpeed"]."</td><td>".$row["DownStdDev"]."</td><td>".$row["DownMedian"]."</td><td>".$row["DownPeriod"]."</td><td>".$row["DownPct"]."</td><td>".$row["ErrorType"]."</td></tr>";
         }
         echo "</table>";
     }
     else
     {
         echo "No data for this test";
     }

     echo "<h1>UDP Results</h1>";

     $sql = "SELECT * FROM UDPResults";
     $result = $conn->query($sql);

     if ($result->num_rows > 0)
     {
         // output data of each row
         echo "<table border=1><tr><td>ConnectionLoc</td><td>TestNumber</td><td>Port</td><td>DatagramSize</td><td>Jitter</td><td>Loss</td><td>Time</td><td>ErrorType</td></tr>";
         while($row = $result->fetch_assoc())
         {
             echo "<tr><td>".$row["ConnectionLoc"]."</td><td>".$row["TestNumber"]."</td><td>".$row["Port"]."</td><td>".$row["DatagramSize"]."</td><td>".$row["Jitter"]."</td><td>".$row["Loss"]."</td><td>".$row["Time"]."</td><td>".$row["ErrorType"]."</td></tr>";
         }
         echo "</table>";
     }
     else
     {
         echo "No data for this test";
     }



    $conn->close();



    ?>




</body>
</html>
