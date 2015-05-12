
<?php
if (isset($_POST['submit'])) {
    require("/home/ubuntu/csdi_main/_db_conn_default.php");
    //create connection
    $db = getConn();
    //Returns object to connect to
    $sql = "INSERT INTO `HelpRequest`
            (`ContactName`, `ContactEmail`, `ErrorType`, `ErrorMessage`)
            VALUES
            (:name, :email, :error, :message)";
    $namedParameters = array(':name' => $_POST['name'],
                             ':email' => $_POST['email'],
                             ':error' => $_POST['subject'],
                             ':message' => $_POST['message']);
    $stmt = $db->prepare($sql);
    $stmt->execute($namedParameters);

#Now we use the HTML
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="description" content="">
        <meta name="author" content="Nicholas Moradi">
        <meta http-equiv="refresh" content="0; url=./home.php" />
    </head>
    <body>
        <hr/>
        <footer>
            <div class="container">
                <p class="text-muted credit">Website designed and built by Peter Walker, Timothy Dyck, and Nicholas Moradi.</p>
                <p class="text-muted credit">Senior Capstone project of <a href="https://csumb.edu/">California State University of Monterey Bay</a>, 2015.</p>
            </div>
        </footer>
    </body>
</html>
<?php
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#End of HTML in IF

} else {
#Now we use the HTML
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Contacts</title>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <meta name="keywords"
              content="HTML, data analysis, cpuc, CPUC, csumb, CSUMB">
        <meta name="description" content="">
        <meta name="author" content="Nicholas Moradi">

        <!-- Latest jQuery -->
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet"
              href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.css">
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.js"></script>
        <!-- Google captcha API -->
        <script src='https://www.google.com/recaptcha/api.js'></script>

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
                    <div class="navbar-header">
                        <button type="button"
                                class="navbar-toggle collapsed"
                                data-toggle="collapse" data-target="#navbar"
                                aria-expanded="false" aria-controls="navbar">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand" href="#">CSDI</a>
                    </div>
                    <div id="navbar" class="navbar-collapse collapse">
                        <ul class="nav navbar-nav">
                            <li><a href="home.php">Home</a></li>
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
                            <li class="active"><a href="contact.php">Help/Contact</a></li>
                        </ul>
                        <!--
                        <form class="navbar-form navbar-left" role="search">
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="Search">
                            </div>
                            <button type="submit" class="btn btn-default">Submit</button>
                        </form>
                        -->
                    </div> <!-- /.nav-collapse -->
                </div> <!-- END CONTAINER -->
            </nav>


            <form method="post">
                <fieldset style ="width: 400px; margin:  0px auto;">
                    <legend>Help/Contact Page</legend>
                    Name: <input type='text' name='name' placeholder='Enter Name' required> <br />
                    Email: <input type='text'name='email' placeholder='Enter Email' required> <br />
                    Subject Matter
                    <select name='subject'>
                        <option value="Data_Error"> Data Error </option>
                        <option value="Graph_Error"> Graph Error </option>
                        <option value="Website_Bug"> Website Bug </option>
                        <option value="Other"> Other </option>
                    </select>
                    <br />

                    <textarea name="message" rows="6" cols="50" align="right center">
                        Enter Message here</textarea>
                    <form method="get" action="contact_help/verify.php">
                        <div class="g-recaptcha"
                             data-sitekey="6LdzMAYTAAAAAAWSwoxglyG3yVYxrESnUKZ8Jwem">
                        </div>
                        <?php
                        /*
                            #This code is to generate the basic type of captcha

                            require_once('contact_help/recaptchalib.php');
                            $publickey = "6LdzMAYTAAAAAAWSwoxglyG3yVYxrESnUKZ8Jwem";
                            echo recaptcha_get_html($publickey);
                        */
                        ?>
                    </form>

                    <br />
                    <input type="submit" name="submit" value="submit" />
                    <p align="left">&copy; Copyright  by Nicholas Moradi</p>

                </fieldset>
            </form>
        </div>

        <hr/>
        <footer>
            <div class="container">
                <p class="text-muted credit">Website designed and built by Peter Walker, Timothy Dyck, and Nicholas Moradi.</p>
                <p class="text-muted credit">Senior Capstone project of <a href="https://csumb.edu/">California State University of Monterey Bay</a>, 2015.</p>
            </div>
        </footer>
    </body>
</html>
<?php
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#End of HTML in ELSE
}
?>
