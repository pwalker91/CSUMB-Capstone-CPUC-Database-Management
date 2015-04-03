<html>
<head>
    <title>CalSpeed Data Imaging</title>

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
    <h1>Welcome to CalSpeed Data Imaging</h1>
    <img src="202.png"><br/>
    <table border=1>
        <tr>
            <td colspan=3>
                Bacon ipsum dolor amet venison pastrami strip steak pig. Andouille porchetta short loin jerky t-bone jowl corned beef hamburger pork belly pig tenderloin landjaeger meatloaf tail short ribs. Shoulder drumstick t-bone porchetta, ribeye pastrami frankfurter bresaola kielbasa ground round flank pancetta turducken. Meatball biltong venison drumstick sausage tri-tip flank
                <br/>
                Short loin turkey ham hock, kielbasa turducken meatball landjaeger. Turducken pork loin cow, swine porchetta hamburger sausage beef ribs leberkas. Beef leberkas pork chop hamburger flank fatback sausage rump pastrami pork loin kielbasa prosciutto short ribs. Corned beef meatloaf doner, bacon brisket shank tri-tip boudin pork belly prosciutto. Meatloaf alcatra bresaola hamburger pig ball tip shoulder shank pastrami ham hock kevin cupim flank frankfurter. Swine flank alcatra spare ribs boudin.

            </td>
        </tr>
        <tr>
            <td>
                <center>
                <table border=4 alignment=center>
                    <tr>

                        <?php
                            $sql = "SELECT *
                            FROM PageResults
                            WHERE 1
                            ";
                            $result = $conn->query($sql);
                            while($row = $result->fetch_assoc()) {
                                echo '<td><img src="http://hosting.otterlabs.org/classes/dycktimothya/cpuc/'.$row["ImagePath"]. '" height="300" width ="300"/></td>';}
    
                            ?>
                    </tr>
                </table>
                </center>
            </td>
        </tr>
        <tr>
            <td>
                <center>
                    <h1>Make your own analytical querey</h1>
                </center>
                <table border=3>
                    <tr>
                        <td>
Bacon ipsum dolor amet ut shankle voluptate quis, doner aliquip salami meatloaf sint ad kielbasa mollit pork spare ribs consequat. Qui doner anim, adipisicing swine ball tip consequat brisket meatball cow porchetta pork loin. Short loin ground round cupidatat filet mignon frankfurter ex short ribs. Consectetur labore jerky, et salami nulla tenderloin. Brisket anim commodo voluptate, reprehenderit esse exercitation chicken occaecat swine labore hamburger meatloaf picanha.

Ut spare ribs strip steak pork loin cillum. Beef alcatra shankle ea venison ullamco turducken. Et occaecat culpa mollit pig, laborum pork boudin ut swine nisi prosciutto. T-bone officia landjaeger culpa. Aliquip non shank pork belly ham hock magna meatball beef mollit cupidatat ea duis. Non swine pork belly corned beef frankfurter ut brisket incididunt pariatur.

Meatloaf nulla jowl laboris ham hock mollit. Proident incididunt fugiat nisi qui, minim duis. In reprehenderit pork loin fugiat, in adipisicing id chicken. Pancetta meatloaf corned beef sirloin, cupidatat id porchetta sausage pastrami pork pork loin in magna. Eiusmod chicken strip steak capicola bresaola cillum. Minim shankle pariatur kielbasa commodo consectetur.
                        </td>
                    </tr>
                </table>
                <center>
                    <button type="button"><a href="http://www.google.com">Click Me!</a></button>
                </center>
            </td>
        </tr>
        <tr>
            <td>
                <center>
                    </br><h3>Help Page</h3>
                    </br><h3>About</h3>
                </center>
            </td>
        </tr>


    </table>


    

    </center>


</body>
</html>