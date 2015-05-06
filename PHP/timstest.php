<!DOCTYPE html>
<html>
<body>

<?php

$var="Hello,  world";
echo $var;
echo "<br/>";
$var=substr_replace($var ,"moo",0,7); // 0 will start replacing at the first character in the string
echo $var;

?>

</body>
</html>
