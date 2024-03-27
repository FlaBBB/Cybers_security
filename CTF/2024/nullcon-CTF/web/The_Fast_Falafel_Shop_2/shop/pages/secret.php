<?php
if (isset($_POST["url"])) {
  exec("python3 /opt/admin.py " . escapeshellarg($_POST["url"]) . " > /dev/null &");
  echo "Visiting url...";
  die();
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FalafelShop</title>
  <link rel="stylesheet" href="style.css">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
</head>

<body>
  <?php include "navbar.php"; ?>
  <div class="d-flex justify-content-center", style="margin-bottom: 100px;">
    <h1 id="title">Contact the Admin with your Secret!</h1>
  </div>
  <div class="d-flex justify-content-center">
    <form class="row g-3" action="" method="POST">
      <div class="col-auto">
        <label for="url" class="visually-hidden">URL</label>
        <input type="text" name="url" class="form-control" id="url" placeholder="Secret URL">
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary mb-3">Submit</button>
      </div>
    </form>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
    crossorigin="anonymous"></script>
</body>

</html>