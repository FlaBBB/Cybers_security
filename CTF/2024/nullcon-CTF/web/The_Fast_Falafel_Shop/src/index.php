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
  <?php include 'navbar.php'; ?>
  <section>
    <div class="bg-light" style="margin-bottom: 100px;">
      <div class="d-flex justify-content-center">
        <h1>Gallery</h1>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <div id="carouselExampleAutoplaying" class="carousel-fade" data-bs-ride="carousel">
        <div style="border: 1px solid black;">
          <div class="carousel-inner">
            <div class="carousel-item active">
              <img src="/images/falafel1.jpg" width="650ex" height="650ex" alt="wcyd">
            </div>
            <div class="carousel-item">
              <img src="/images/falafel2.jpg" width="650ex" height="650ex" alt="wcyd">
            </div>
            <div class="carousel-item">
              <img src="/images/falafel3.jpg" width="650ex" height="650ex" alt="wcyd">
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section style="margin-top: 100px;">
    <div class="bg-light">
      <div class="d-flex justify-content-center">
        <h1 id="products_and_pricing">Products and Pricing</h1>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <table class="table table-striped" style="margin-top: 100px; width: 80%; border: 1px solid black;">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Small</th>
            <th scope="col">Big</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>Falafel wrap</td>
            <td>$5</td>
            <td>$6</td>
          </tr>
          <tr>
            <td>Falafel box</td>
            <td>$7</td>
            <td>$9</td>
          </tr>
          <tr>
            <td>Falafel balls</td>
            <td>$3 (6 pieces)</td>
            <td>$5 (12 pieces)</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
  <br>
  <br>
  <br>
  <section>
    <div class="bg-light">
      <div class="d-flex justify-content-center">
        <h1 id="about_us">About us</h1>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <p class="d-flex justify-content-center" style="width: 80%;">This website is dedicated to our beloved @gehaxelt,
        who is insanely in love with Falafel.</p>
    </div>

  </section>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
    crossorigin="anonymous"></script>
</body>

</html>