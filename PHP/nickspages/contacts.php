
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">

  <!-- Always force latest IE rendering engine (even in intranet) & Chrome Frame 
       Remove this if you use the .htaccess -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title>Contacts</title>
  <meta name="description" content="">
  <meta name="author" content="Nicholas Moradi">

  <meta name="viewport" content="width=device-width; initial-scale=1.0">

  <!-- Replace favicon.ico & apple-touch-icon.png in the root of your domain and delete these references -->
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <script src='https://www.google.com/recaptcha/api.js'></script>
</head>

<body>
  <div>
    <header>
      <h1>Help/Contact</h1>
    </header>
    <nav>
      <p><a href="/">Home</a></p>
      <p><a href="/contact">Contact</a></p>
    </nav>

    <div>
      <form method="post" action="verify.php">
      	<fieldset style = "width: 500px; margin:  0px auto;">
      		<legend>Help/Contact Page</legend>
      		Name: <input type='text' name='Name' placeholder='Enter Name' required> <br />
			Email: <input type='text'name='email' placeholder='Enter Email' required> <br />
			Subject Matter
			<select name = 'subject'>
				<option value="Data_Error"> Data Error </option>
    			<option value="Graph_Error"> Graph Error </option>
    			<option value="Website_Bug"> Website Bug </option>
    			<option value="Other"> Other </option>
    			 
			</select>
			<br />
			<textarea name="Message" rows="6" cols="50">
				Enter Message here
			</textarea>
			<br />
			<?php
    			 require_once('recaptchalib.php');
     			 $publickey = "6LcXzgQTAAAAAKSUbd_RVGpAdxDKiXD4SEpn9nrK"; // you got this from the signup page
    			 echo recaptcha_get_html($publickey);
  			?>
			<br />
			<input type="submit" value="Submit">
      	</fieldset>
      </form>
    </div>

    <footer>
     <p>&copy; Copyright  by Nicholas Moradi</p>
    </footer>
  </div>
</body>
</html>
