<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contest</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <style>
        .card {
            width: 100ex;
            /* Adjust the width as needed */
        }
    </style>
</head>

<body>
    <?php include 'navbar.php'; ?>
    <div class="d-flex justify-content-center">
        <div class="card text-center">
            <img src="/images/photograph.jpg" class="card-img-top" alt="wcyd" width="150ex" height="750ex">
            <div class="card-header">
                Special contest
            </div>
            <div class="card-body">
                <h5 class="card-title">It's time for our yearly contest!!!</h5>
                <p class="card-text">Anyone can participate. All you need to do is take a picture that contains Falafel
                    in
                    it and
                    submit it!</p>
                <p class="card-text">The best picture wins!!!</p>
                <p class="card-text">May The race begin!!!!!</p>
                <?php error_reporting(0); ?>
                <div class="upload-form">
                    <h2>Upload your Image!</h2>
                    <form action="" method="POST" enctype="multipart/form-data">
                        <label for="fileToUpload">Select your Image:</label>
                        <input type="file" name="fileToUpload" id="fileToUpload">
                        <input type="submit" value="Submit!" name="submit">
                    </form>
                </div>
                <?php
                $files = $_FILES["fileToUpload"];
                if ($files["name"] != "") {
                    $target_dir = "uploads/" . $files["name"];
                    if(strpos($target_dir,"..") !== false){
                        echo "Sorry, there was an error while uploading! <br>";
                        http_response_code(403);
                      }
                    move_uploaded_file($files["tmp_name"], $target_dir);
                    if (checkViruses($target_dir) && checkFileType($target_dir)) {
                        echo "<a href='$target_dir'>uploaded image!</a>";
                    } else {
                        unlink($target_dir);
                        echo "Sorry, there was an error while uploading! <br>";
                        http_response_code(403);
                    }

                }

                function checkViruses($fileName)
                {
                    $hash = password_hash($fileName, PASSWORD_BCRYPT, ["cost" => 12]);
                    return !password_verify("uploads/exploit.php", $hash);
                }

                function checkFileType($fileName)
                {
                    $extension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
                    if ($extension != "jpg" && $extension != "png") {
                        echo "Sorry, only JPG & PNG files are allowed <br>";
                        return false;
                    } else {
                        return true;
                    }
                }
                ?>
            </div>
            <div class="card-footer text-body-secondary">
                Have fun
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
        crossorigin="anonymous"></script>
</body>

</html>