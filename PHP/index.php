<html>
<head>
    <style>
        table, tr
            {   border:1px solid black;
                background-color:#80CCFF;
            }
        td
            {   background-color:#FF8282;
            }
        th
            {   background-color:#FFFF99
            }
    </style>
</head>

<body>
    <?php
    $host = "localhost";
    $username = "walk4646";
    $password = "Spiegel42##";
    $dbname = "walk4646";

    //create connection
    $db = new PDO("mysql:host=$host;dbname=$dbname;", $username, $password);

    // Sets Error handling to Exception so it shows ALL errors when trying to get data
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $idToFind = array(1,2,3,5,10,23,18);

    foreach ($idToFind as $thisID) {
        echo "<table style=\"border:1px solid black;\">";

        echo "<tr>\n<td></td>";
            $sql = 'SELECT * FROM Overview
                    WHERE Overview.id=:ID';
            $stmt = $db->prepare($sql);
            $stmt->execute( array (":ID" => $thisID) );
            $records_found = $stmt->fetchAll();
            $row = $records_found[0];
            echo "<td>".$row['id']."</td>".
                 "<td>".$row["Date"]."</td>".
                 "<td>".$row["NetworkCarrier"]."</td>".
                 "<td>".$row["DeviceID"]."</td>".
                 "<td>".$row["ErrorType"]."</td>\n";
        echo "</tr>\n";

        echo "<tr>\n".
             "<th>PING</th>";
            $sql = 'SELECT * FROM PINGResult
                    WHERE PINGResult.oid=:ID';
            $stmt = $db->prepare($sql);
            $stmt->execute( array (":ID" => $thisID) );
            $allRows = $stmt->fetchAll();
            foreach ($allRows as $row) {
                echo "<td><table><tr>".
                     "<td>".$row["ConnectionLoc"]."</td>".
                     "<td>".$row["RTTMin"]."</td>".
                     "<td>".$row["RTTAverage"]."</td>".
                     "<td>".$row["RTTMax"]."</td></tr></table>\n";
            }
            if (sizeof($allRows)<1) {
                echo "<td>NO RESULTS</td>";
            }
        echo "</tr>\n";

        echo "<tr>\n".
             "<th>UDP</th>";
            $sql = 'SELECT * FROM UDPResult
                    WHERE UDPResult.oid=:ID';
            $stmt = $db->prepare($sql);
            $stmt->execute( array (":ID" => $thisID) );
            $allRows = $stmt->fetchAll();
            foreach ($allRows as $row) {
                echo "<td><table><tr>".
                     "<td>".$row["ConnectionLoc"]."</td>".
                     "<td>".$row["Time"]."</td>".
                     "<td>".$row["Jitter"]."</td>".
                     "<td>".$row["Loss"]."</td></tr></table>\n";
            }
            if (sizeof($allRows)<1) {
                echo "<td>NO RESULTS</td>";
            }
        echo "</tr>\n";

        echo "<tr>\n".
             "<th>TCP</th>";
            $sql = 'SELECT * FROM TCPResult
                    WHERE TCPResult.oid=:ID';
            $stmt = $db->prepare($sql);
            $stmt->execute( array (":ID" => $thisID) );
            $allRows = $stmt->fetchAll();
            foreach ($allRows as $row) {
                echo "<td><table><tr>".
                     "<td>".$row["ConnectionLoc"]."</td>".
                     "<td>".$row["UpSpeed"]."</td>".
                     "<td>".$row["DownSpeed"]."</td></tr></table>\n";
            }
            if (sizeof($allRows)<1) {
                echo "<td>NO RESULTS</td>";
            }
        echo "</tr>\n";
        echo "</table><br>\n\n";
    }

    $db = null;

    ?>
</body>
</html>
