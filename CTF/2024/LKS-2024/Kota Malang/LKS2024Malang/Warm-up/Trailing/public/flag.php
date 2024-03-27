<?php
include 'config.php';
session_start();

$stmt = $conn->prepare("SELECT user FROM tb_user WHERE user = ? LIMIT 1") or die(mysqli_error($conn));
$stmt->bind_param("s", $_SESSION['user']) or die(mysqli_error($conn));
$res = $stmt->execute() or die(mysqli_error($conn));
if($res){
	$stmt->bind_result($result) or die(mysqli_error($conn));
	$stmt->fetch();
	if($result == "admin"){
		die("FLAG");
	}
	else{
		die("you are not an admin");
	}
}else{
	echo "you are not admin";
}
?>
