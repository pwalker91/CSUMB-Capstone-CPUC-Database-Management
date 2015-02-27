<?php

include('./_db_conn_default.php');

$info = array();

//Getting the overview information
$sql = 'SELECT * FROM Overview WHERE Overview.Date=:Date';
$stmt = $db->prepare($sql);
$stmt->execute( array (":Date" => $_POST['date']) );
$records_found = $stmt->fetchAll();
if (sizeof($records_found) > 0) {
    foreach ($records_found as $row) {
        $thisID = $row['id'];
        $info[$thisID] = array();
        $info[$thisID]["OVR"] = $row;

        //Getting the PING information
        $info[$thisID]["PING"] = array();
        $sql = 'SELECT * FROM PINGResult WHERE PINGResult.oid=:ID';
        $stmt = $db->prepare($sql);
        $stmt->execute( array (":ID" => $thisID) );
        $allRows = $stmt->fetchAll();
        foreach ($allRows as $row) {
            $info[$thisID]["PING"][] = $row;
        }

        //Getting the UDP information
        $info[$thisID]["UDP"] = array();
        $sql = 'SELECT * FROM UDPResult WHERE UDPResult.oid=:ID';
        $stmt = $db->prepare($sql);
        $stmt->execute( array (":ID" => $thisID) );
        $allRows = $stmt->fetchAll();
        foreach ($allRows as $row) {
            $info[$thisID]["UDP"][] = $row;
        }

        //Getting the UDP information
        $info[$thisID]["TCP"] = array();
        $sql = 'SELECT * FROM TCPResult WHERE TCPResult.oid=:ID';
        $stmt = $db->prepare($sql);
        $stmt->execute( array (":ID" => $thisID) );
        $allRows = $stmt->fetchAll();
        foreach ($allRows as $row) {
            $info[$thisID]["TCP"][] = $row;
        }
    }
}

echo json_encode($info);

$db = null;
?>
