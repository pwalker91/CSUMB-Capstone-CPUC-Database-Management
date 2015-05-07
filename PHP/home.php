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

            <div class='row'>
                <div class='col-xs-12 col-sm-8 col-sm-offset-2'>
                    <h3>Request Page</h3>
                    <p>
                        The purpose of this page is to request what kind of graph you would like created, and with what subset of information from our data repository.
                    </p>
                    <p>
                        Our data repository contains a wealth of data collected by the California Public Utilities Commission on the performance of four major Cellular Network Carriers. The Carriers tested were AT&amp;T, Verizon, T-Mobile, and Sprint.
                    </p>
                    <p>
                        From the data collected, which has been parsed into a form of structured data, we can gather information pertaining to the relative performance of each carrier across multiple dimensions. The form on the Request Page will allow you to specify the filtering values across these dimensions.
                    </p>
                    <p>
                        Upon successful generation of a graph showing the performance of the Carriers chosen, a link to the corresponding webpage will be generated and emailed to you, provided that you include a valid email address at the end of the form.
                    </p>
                </div>
            </div>

            <div class='row'>
                <div class='col-xs-12 col-sm-8 col-sm-offset-2'>
                    <h3>Example Graphs</h3>
                    <p>
                        Below are some example graphs that have been generated by previous requests.
                    </p>
                </div>
            </div>

            <div class='row'>
                <div class='col-xs-4'>
                    <img width='300'
                         src='./images/graphs/20150507013315_438871.png' />
                </div>
                <div class='col-xs-4'>
                    <img width='300'
                         src='./images/graphs/20150507014430_468083.png' />
                </div>
                <div class='col-xs-4'>
                    <img width='300'
                         src='./images/graphs/20150507052329_340430.png' />
                </div>
            </div>

        </div>

        <hr/>
        <footer>
            <div class="container">
                <p class="muted credit">Website designed and built by Peter Walker, Timothy Dyck, and Nicholas Moradi.</p>
                <p class="muted credit">Senior Capstone project of <a href="https://csumb.edu/">California State University of Monterey Bay</a>, 2015.</p>
            </div>
        </footer>
    </body>
</html>
