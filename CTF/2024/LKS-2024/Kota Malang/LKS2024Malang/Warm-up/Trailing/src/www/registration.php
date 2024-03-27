<?php
include 'config.php';
if(isset($_POST['username']) && isset($_POST['password'])){
	$username = $_POST['username'];
	$password = $_POST['password'];
	if($username == "admin"){
		die("cannot register as admin");
	}
	$stmt = $conn->prepare("INSERT INTO tb_user (user,password) values (?,?)") or die(mysqli_error($conn));
	$stmt->bind_param("ss", $username, $password) or die(mysqli_error($conn));
	$res = $stmt->execute() or die(mysqli_error($conn));
	if($res){
		header('location:login.php');
	}else{
		die($res);
	}
}
?>
<!DOCTYPE HTML>
<html>
    <head>
        <title>Halaman Registrasi</title>
        <link rel="stylesheet" href="style.css">
    </head>
   
    <body>
        <div class="container">
          <h1>Register</h1>
            <form action="registration.php" method="post">
                <label>Username</label><br>
                <input type="text" id="username" name="username"><br>
                <label>Password</label><br>
		<input type="password" id="password" name="password"><br>
		<input type="submit" value="Registrasi" class="tombol">
            </form>
	</div>
	<a href="logout.php">Logout</a>	
    </body>
</html>
