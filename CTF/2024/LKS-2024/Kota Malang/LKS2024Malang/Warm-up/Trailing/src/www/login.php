<?php
include 'config.php';

if(isset($_POST['username']) && isset($_POST['password'])){
	$username = $_POST['username'];
	$password = $_POST['password'];

	$stmt = $conn->prepare("SELECT * FROM tb_user WHERE user = ? AND password = ?") or die(mysqli_error($conn));
	$stmt->bind_param("ss", $username, $password) or die(mysqli_error($conn));
	$res = $stmt->execute() or die(mysqli_error($conn));
	if($res){
		$result = $stmt->get_result() or die(mysqli_error($conn));
		$num_rows = $result->num_rows or die(mysqli_error($conn));
	}
	if($num_rows > 0){
		$_SESSION['user'] = $username;
		header("Location: flag.php");
	}
}
?>
<!DOCTYPE HTML>
<html>
    <head>
        <title>Halaman Login</title>
        <link rel="stylesheet" href="style.css">
    </head>
   
    <body>
        <div class="container">
          <h1>Login</h1>
            <form action="login.php" method="post">
                <label>Username</label><br>
                <input type="text" name="username" id="username"><br>
                <label>Password</label><br>
		<input type="password" name="password" id="password"><br>
		<input type="submit" value="Login" class="tombol">
            </form>
	</div>
	<a href="logout.php">Logout</a>   
    </body>
</html>
