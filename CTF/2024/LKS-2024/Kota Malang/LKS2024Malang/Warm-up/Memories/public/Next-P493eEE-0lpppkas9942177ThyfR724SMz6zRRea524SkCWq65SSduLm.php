<?php
error_reporting(0);
if (isset($_GET['source'])) {
  highlight_file(__FILE__);
  die();
}
define('APP_RAN', true);
require('flag2.php');

if (!isset($_COOKIE['user'])) {
    $common_user = new User_LKS2024;
    $_COOKIE['user'] = base64_encode(serialize($common_user));
    setcookie(
      'user',
      base64_encode(serialize($common_user)),
      time() + 1 * 30 * 24 * 3600, "/"
    );
  }
   
  if (isset($_POST['user'])) {
    setcookie(
      'user',
      $_POST['user'],
      time() + 1 * 30 * 24 * 3600, "/"
    );
  }
?>
<!DOCTYPE html>
<head>
    <style>
        #title {
    display: flex;
    align-items: center;
    flex-direction: column;
    }
    </style>
    <title>Base64-Encoder</title>
</head>
<body>
  <!--?source-->
    <h1 id="title">Simple Bad Base64 Encoder</h1>
    <br>
    <p>Just Input your text here</p>
    <form action="/Next-P493eEE-0lpppkas9942177ThyfR724SMz6zRRea524SkCWq65SSduLm.php" method="post">
    <textarea type="text" name="user"></textarea>
    <input type="submit">
    </form>
    <p>"Please input twice to make sure encode process successful"</p>
    <?php
class User_LKS2024
{
  public $cookie_type = 'User_LKS2024';
  public function is_admin()
  {
    if ($this->cookie_type == 'Admin-LKS2024') {
      return true;
    } else {
      return false;
    }
  }
  public function __sleep()
  {
    return array($this->cookie_type);
  }
}
?>
<?php
if (isset($_COOKIE['user']) || isset($_POST['user'])) {
  echo "<p>Output:<br/>" . base64_encode($_COOKIE['user']) . '</p>';
} else {
  echo '';
}
?>
<?php
if (isset($_COOKIE['user'])) {
  try {
    $user = unserialize(base64_decode($_COOKIE['user']));
    if ($user->is_admin()) {
      echo '<h3 class="success">Nih Hadiah Buat Kamu,</h3>';
      your_flag();
    } else {
      echo '';
    }
  } catch (Error $e) {
    echo '<h3>Encode Success';
  }
}
?>
</body>
