<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <meta name='author'
              content='Peter Walker | pwalker@csumb.edu'>
        <meta name="keywords"
              content="HTML, data analysis, cpuc, CPUC, csumb, CSUMB">
        <title>CalSpeed Data Imaging Prototype</title>

        <!-- Latest jQuery -->
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet"
              href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.css">
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.js"></script>

        <!-- Some specialty styling -->
        <link rel="stylesheet" href="http://54.200.224.217/csdi/_csdi_style.css" />
    </head>

    <body>
        <div class='container' name='page_container' id='page_container'>
            <div class='row'>
                <div class='jumbotron text-center clear'>
                    <br/>
                    <img src="images/logo.png" height="100">
                    <h1>CalSPEED Data Imaging</h1>
                    <p>Tranforming the way you analyze California Cellular Network Performance</p>
                </div> <!-- end JUMBOTRON -->
            </div> <!-- end ROW -->

            <nav class="navbar navbar-default navbar-fixed-top">
                <div class="container">
                    <!-- Brand and toggle get grouped for better mobile display -->
                    <div class="navbar-header">
                        <a class="navbar-brand" href="#">CSDI</a>
                    </div>

                    <!-- Collect the nav links, forms, and other content for toggling -->
                    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                        <ul class="nav navbar-nav">
                            <li class="active"><a href="home.php">Home</a></li>
                            <li><a href="request.php">Request</a></li>
                            <li class="dropdown">
                                <a href="#"
                                   class="dropdown-toggle"
                                   data-toggle="dropdown"
                                   role="button"
                                   aria-expanded="false">Results<span class="caret"></span>
                                </a>
                                <ul class="dropdown-menu" role="menu">
                                    <li><a href="#">Recent Results</a></li>
                                    <li><a href="#">Popular Results</a></li>
                                </ul>
                            </li>
                            <li><a href="contact.php">Help/Contact</a></li>
                        </ul>
                        <!--
                        <form class="navbar-form navbar-left" role="search">
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="Search">
                            </div>
                            <button type="submit" class="btn btn-default">Submit</button>
                        </form>
                        -->
                    </div>
                </div> <!-- END CONTAINER -->
            </nav>



        <table>
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
                          /*
                            $sql = "select * from PageResults order by Id desc limit 3";
                            $result = $conn->query($sql);
                            while($row = $result->fetch_assoc()) {
                            $var=substr_replace($row["ImagePath"] ,"",0,59);

                            echo '<td><img src="./images' .$var. '" height="300" width ="300"/></td>';}
                            */
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
                        <a href="request.php">Make your Own Analytical Query</a>
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
                        <a href="result.php?d=c4ca4238a0">See Some Results</a>
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

        </div>
    </body>
</html>
