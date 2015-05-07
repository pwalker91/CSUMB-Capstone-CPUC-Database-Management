<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <meta name='author'
              content='Timothy Dyck'>
        <meta name="keywords"
              content="HTML, data analysis, cpuc, CPUC, csumb, CSUMB">
        <title>Results</title>

        <!-- Latest jQuery -->
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet"
              href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.css">
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.js"></script>

        <!-- Some specialty styling -->
        <link rel="stylesheet" href="./_csdi_style.css" />
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
                            <li><a href="home.php">Home</a></li>
                            <li><a href="request.php">Request</a></li>
                            <li class="dropdown active">
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
        </div>


        <?php
        if (isset($_GET['h'])) {
            include("_db_conn_default.php");
            $db = getConn();

            $sql = "SELECT *
                    FROM PageResults
                    WHERE PageHash=:pagehash";
            $opts = array(":pagehash" => $_GET['h']);

            $stmt = $db->prepare($sql);
            $stmt->execute($opts);
            $result = $stmt->fetchAll();

            if (empty($result)) {
                ?>

                <div class='row'>
                <div class='col-xs-3'></div>
                <div class='col-xs-6 text-center'>
                    <p style="font-size: 140%;">
                        <b>We're sorry.</b><br/>
                        There are no results associated with this link.<br/><hr/>
                        Please consider going to the <a href="request.php" class="alert-link">Request Page</a> to complete<br/>
                        the form for requesting new analyses.
                    </p>
                </div>
                </div>

                <?php
            } else {
                $result = $result[0];
                $imagePath = str_replace("/home/ubuntu/csdi_www",
                                         "http://54.200.224.217/csdi/",
                                         $result['ImagePath']);
                #Decoding JSON. The 'true' is so that we get an array rather than an object
                $meta = json_decode($result['MetaInfo'], true);
                ?>

                <div class='row'>
                    <div class='col-xs-12 text-center'>
                        <img src=<?=$imagePath;?> />
                    </div>
                </div>
                <hr />

                <div class='row'>
                    <div class='col-xs-12 col-sm-4 col-sm-offset-4 text-center'>
                        <table class='table'>
                            <tr>
                                <th>Total Number of Data Points</th>
                                <td><?=$meta['dataPoints'];?></td>
                            </tr>
                            <tr>
                                <th>Number of Test Files Used</th>
                                <td><?=$meta['filesUsed'];?></td>
                            </tr>
                        </table>
                    </div>
                </div>

                <div class='row'>
                    <div class='col-xs-12 col-sm-6 col-sm-offset-3 text-center'>
                        <p>
                            To request more information, please fill out the <a href='contact.php'>Contact</a> form with the current URL.
                        </p>
                    </div>
                </div>

                <?php
            }
        } else {
            ?>

            <div class='row'>
            <div class='col-xs-3'></div>
            <div class='col-xs-6 text-center'>
                <p style="font-size: 140%;">
                    <b>Welcome to the Results Page.</b><br/>
                    This page requires a URL variable to show results.<br/><hr/>
                    Please consider going to the <a href="request.php" class="alert-link">Request Page</a> to complete<br/>
                    the form for requesting new analyses.
                </p>
            </div>
            </div>

            <?php
        }
        ?>

        <hr/>
        <footer>
            <div class="container">
                <p class="muted credit">Website designed and built by Peter Walker, Timothy Dyck, and Nicholas Moradi.</p>
                <p class="muted credit">Senior Capstone project of <a href="https://csumb.edu/">California State University of Monterey Bay</a>, 2015.</p>
            </div>
        </footer>
    </body>
</html>
