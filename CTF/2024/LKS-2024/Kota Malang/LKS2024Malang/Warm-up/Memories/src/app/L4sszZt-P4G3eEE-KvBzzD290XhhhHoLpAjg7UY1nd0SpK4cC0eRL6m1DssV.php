<?php
if (isset($_GET['source'])) {
  highlight_file(__FILE__);
  die();
}
require('flag3.php');
error_reporting(0);

function correct_login()
{
  $username = (string)$_GET['username'];
  $password = (string)$_GET['password'];

  if ($username === $password) return false;
  if (sha1($username) === sha1($password)) return true;

  return false;
}

?>

<!DOCTYPE html>

<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css">
  <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
  <title>Login Page</title>
</head>

<body>
  <!--?source-->
  <section class="hero">
    <div class="container">
      <div class="hero-body">
        <h1 class="title">Another Login Pages</h1>
      </div>
    </div>
  </section>


  <div class="container" style="margin-top: 3em; margin-bottom: 3em;">
    <div class="columns is-centered">
      <div class="column is-8-tablet is-8-desktop is-5-widescreen">
        <form>
          <div class="field">
            <p class="control has-icons-left has-icons-right">
              <input class="input" type="text" placeholder="Username" name="username">
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </p>
          </div>
          <div class="field">
            <p class="control has-icons-left">
              <input class="input" type="password" placeholder="Password" name="password">
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
            </p>
          </div>
          <input class="button" type="submit" value="Sign In">
        </form>
      </div>
    </div>

    <?php if (isset($_GET['username']) and isset($_GET['password'])) : ?>
      <div class="columns is-centered">
        <p>:)</p>
        <?php if (correct_login()) : ?>
          <p>Selamat!</p>
          <?php die(your_flag()); ?>
        <?php else : ?>
          <p>Forgot your Password? <a href="https://www.youtube.com/watch?v=BBJa32lCaaY">Here</a></p>
        <?php endif; ?>
      </div>
    <?php endif; ?>
  </div>
</body>
