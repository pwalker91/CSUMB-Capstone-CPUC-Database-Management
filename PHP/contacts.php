
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
  <!-- <script src='https://www.google.com/recaptcha/api.js'></script> -->
  <script src='https://www.google.com/recaptcha/api.js'></script>
<style>
body {
    background-image: url('images/wireless-tower.jpg');
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: 72% 66%;
}
</style>
</head>

<body>
  <div>
    <header>
      <center><h1>Help/Contact</h1>
    </header>
    <nav>
      <center>
      <a href="/">Home</a>
      <a href="contacts.php">Contact</a>
      </center>
</nav></center>

    <div>
      <form method="get" action="check.php">
      	<fieldset style ="width: 400px; margin:  0px auto;">
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
			<textarea name="Message" rows="6" cols="50" align="right center">Enter Message here</textarea>
      <form methd="get" action="verify.php">
      <div class="g-recaptcha" data-sitekey="6LdzMAYTAAAAAAWSwoxglyG3yVYxrESnUKZ8Jwem"></div>
			<!--<?php
    			 require_once('recaptchalib.php');
     			 $publickey = "6LdzMAYTAAAAAAWSwoxglyG3yVYxrESnUKZ8Jwem"; // you got this from the signup page
    			 echo recaptcha_get_html($publickey)
  			?>-->
      </form
			<br />
		<input type="submit" name="submit" value="submit" />
		<p align="left">&copy; Copyright  by Nicholas Moradi</p>
      	</fieldset>
      </form>
    </div>

    <footer>
    </footer>
  </div>
</body>
</html>
