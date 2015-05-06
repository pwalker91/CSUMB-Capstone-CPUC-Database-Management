<?
    include("./.db_conn_default.php");
?>
<html>
<head>
    <title>CalSpeed Data Imaging</title>
    <?php
        $servername = "localhost";
        $username = "root";
        $password = "cpuc";
        $dbname = "cpuc";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
    ?>
<style>
body {
    background-color: #000000;
    background-image: url('images/wireless-tower.jpg');
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position:66% 70%;
}
.doda {

//    text-outline: 2px 2px #ffffff;

color: black;
    text-shadow:
    -.75px -.75px 0 #fff,
    .75px -.75px 0 #fff,
    -.75px .75px 0 #fff,
    .75px .75px 0 #fff;  

}

</style>
</head>
<body">
    <center>
    <h1 class="doda">Welcome to CalSpeed Data Imaging</h1>
    <img src="images/CalSpeed.png" height="100"><br/>
    <br />
    <table>
<h3>	<tr>
    		<td width="33%">
			<center>
			<h3>
        		<a href="home.php"> Home</a>
			</h3>
			</center>
		</td>
		<td width="33%">
			<center>
			<h3>
			<a href="analysisRequest/request.php"> Make A Request/Query Page</a>
			</h3>
			</center>
    		</td>
		<td width="33%">
			<center>
			<h3>
			<a href="contacts.php">Help/Contact Page</a>
			</h3>
			</center>
    		</td>
	</tr>	
</h3	
        <tr>
	   <td colspan=3 class="doda" style="font-size:18px">
		<br/>
                <center>Insert Paragraph here about what this is and what this site is designed for...</center>
                <br/>
           </td>
        </tr>
        <tr>
            <td colspan=3>
                <center>
                <table border=4 alignment=center>
                    <tr>
                      <?php
                          $sql = "select * from PageResults order by Id desc limit 3";
                          $result = $conn->query($sql);
                          while($row = $result->fetch_assoc()) {
			     $var=substr_replace($row["ImagePath"] ,"",0,59);

                              echo '<td><img src="./images' .$var. '" height="300" width ="300"/></td>';}

                      ?>

                    </tr>
                </table>
                </center>
            </td>
        </tr>
        <tr>
            <td colspan=3>
                <center>
                <br/>
                    <a href="analysisRequest/request.php">Make your Own Analytical Query</a>
                </center>
                <br/>
                <table border=3 height="100px" width="550px" align="center" bgcolor=#FFFFFF>
                    <tr>
                        <td>
 			<center>
	                         This page is for making a query to our databases. Users can give the query specifics in order to define their query. Users as well can request a graph to be made when the query is generated to see visually what it may look like.
        	                 Explain data and where data comes from. Further explainationof graphs possibly? Some info that further explains CalSPEED Data Imagining
			</center>
                       </td>
                    </tr>
                </table>
                <center>
                <br/>
                    <a href="analysisResults/result.php?d=c4ca4238a0">See Some Results</a>
                <br/>
                <br/>
                </center>
                <center>
                <table border=5 bgcolor=#FFFFFF>
                	<tr>
                    	<td>
				Video of how what do this website coming soon!!!
                        </td>
                    </tr>
                </table>
                </center>
                <!--
                <center>
                    <button type="button"><a href="http://www.google.com">Click Me!</a></button>
                </center>
                -->
            </td>
        </tr>
        <tr>
            <td colspan=3>
                <center>
                </br><a href="contacts.php">Help Page</a>
                </center>
            </td>
        </tr>


    </table>




    </center>


</body>
</html>
