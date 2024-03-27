<?php
error_reporting(0);
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    die();
}

require('flag.php');
$notes = preg_replace('/LKS2024/', '', htmlspecialchars($_POST['Notes']));

?>

<!DOCTYPE html>

<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css">
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
    <title>LKS's Secret Notes</title>
</head>

<body>
    <!--?source-->
    <section class="hero">
        <div class="container">
            <div class="hero-body">
                <h1 class="title">LKS's Secret Notes</h1>
                <h2 class="subtitle">Tulis kenangan indahmu saat bersamanya</h2>
            </div>
        </div>
    </section>

    <div class="container" style="margin-top: 3em; margin-bottom: 3em;">
        <div class="columns is-centered">
            <div class="column is-8-tablet is-8-desktop is-5-widescreen">
                <form method="post">
                    <div class="field">
                        <div class="control">
                            <input class="input is-large" placeholder="Type here" type="text" name="Notes" />
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <div class="columns is-centered">
            <?php if (isset($_POST['Notes'])) : ?>
                <div class="card column is-8-tablet is-8-desktop is-5-widescreen">
                    <div class="card-content">
                        <h3>Isi Notes : <?= $notes ?></h3><br>
                        <?php if ($notes == 'LKS2024') : ?>
                            <p>Sudahilah kegalauanmu, mari kita lomba CTF bersamaku!</p>
                            <?= your_flag() ?>
                        <?php else : ?>
                            <p>Kenanganmu masih terlalu indah untuk diingat</p>
                            <p>Bukan waktunya untuk menangisi-nya</p>
                        <?php endif; ?>
                    </div>
                </div>
            <?php endif ?>
        </div>
    </div>
</body>
