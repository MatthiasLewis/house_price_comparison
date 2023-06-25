<?php
// 建立與 MySQL 的連線
$servername = "localhost";
$username = "admin";
$password = "123456";
$dbname = "houseprice";
$port = 3306;

$connection = mysqli_connect($servername, $username, $password, $dbname, $port);

// 檢查連線是否成功
if (!$connection) {
    die("資料庫連線失敗：" . mysqli_connect_error());
}		


// 選擇資料庫
if (!mysqli_select_db($connection, $dbname)) {
    die("無法選擇資料庫：" . mysqli_error($connection));
}

$limit = 30;
// 取得連結的資料
$query = "select * from buy_Xindian LIMIT $limit";
$result = mysqli_query($connection, $query);

$query2 = "select * from buy_Wenshan LIMIT $limit";
$result2 = mysqli_query($connection, $query2);

$query3 = "select * from rent_Xindian LIMIT $limit";
$result3 = mysqli_query($connection, $query3);

$query4 = "select * from rent_Wenshan LIMIT $limit";
$result4 = mysqli_query($connection, $query4);

// 檢查查詢是否成功
if (!$result) {
// 如果有資料
// 檢查查詢是否成功
    die("資料庫查詢失敗：" . mysqli_error($connection));
}
// 釋放資料庫查到的記憶體
// mysqli_free_result($result);

// 關閉 MySQL 連線
mysqli_close($connection);
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>SEO Master - SEO Agency Website Template</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <meta content="" name="keywords">
    <meta content="" name="description">

    <!-- Favicon -->
    <link href="img/favicon.ico" rel="icon">

    <!-- Google Web Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet"> 

    <!-- Icon Font Stylesheet -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css" rel="stylesheet">

    <!-- Libraries Stylesheet -->
    <link href="lib/animate/animate.min.css" rel="stylesheet">
    <link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">
    <link href="lib/lightbox/css/lightbox.min.css" rel="stylesheet">

    <!-- Customized Bootstrap Stylesheet -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Template Stylesheet -->
    <link href="css/style.css" rel="stylesheet">
</head>

<body>
    <div class="container-xxl bg-white p-0">
        <!-- Spinner Start -->
        <div id="spinner" class="show bg-white position-fixed translate-middle w-100 vh-100 top-50 start-50 d-flex align-items-center justify-content-center">
            <div class="spinner-grow text-primary" style="width: 3rem; height: 3rem;" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <!-- Spinner End -->


        <!-- Navbar & Hero Start -->
        <div class="container-xxl position-relative p-0">
            <nav class="navbar navbar-expand-lg navbar-light px-4 px-lg-5 py-3 py-lg-0">
                <a href="" class="navbar-brand p-0">
                    <img src="https://stickershop.line-scdn.net/stickershop/v1/sticker/199420891/android/sticker.png" style="height:auto;width:100%;margin:0 auto;" alt="Logo">
                    <!-- <img src="img/logo.png" alt="Logo"> -->
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
                    <span class="fa fa-bars"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarCollapse">
                    <div class="navbar-nav ms-auto py-0">
                        <a href="index.html" class="nav-item nav-link">首頁</a>
                        <a href="about.html" class="nav-item nav-link">時程規劃</a>
                        <a href="service.php" class="nav-item nav-link active">資料探索</a>
                        <!--<a href="project.html" class="nav-item nav-link">參考資料</a>-->
                        <div class="nav-item dropdown">
                            <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">分析結果</a>
                            <div class="dropdown-menu m-0">
                                <a href="team.html" class="dropdown-item">當你的朋友問你買房了嗎</a>
                                <a href="testimonial.html" class="dropdown-item">房價飆升 吃土人生</a>
                            </div>
                        </div>
                        <a href="contact.html" class="nav-item nav-link">Contact</a>
                    </div>
                    <butaton type="button" class="btn text-secondary ms-3" data-bs-toggle="modal" data-bs-target="#searchModal"><i class="fa fa-search"></i></butaton>
                    <a href="https://htmlcodex.com/startup-company-website-template" class="btn btn-secondary text-light rounded-pill py-2 px-4 ms-3">Pro Version</a>
                </div>
            </nav>

            <div class="container-xxl py-5 bg-primary hero-header mb-5">
                <div class="container my-5 py-5 px-lg-5">
                    <div class="row g-5 py-5">
                        <div class="col-12 text-center">
			    <h1 class="text-white animated zoomIn">網頁爬蟲清洗結果</h1>
                            <hr class="bg-white mx-auto mt-0" style="width: 90px;">
                            <nav aria-label="breadcrumb">
                                <ol class="breadcrumb justify-content-center">
                                    <li class="breadcrumb-item"><a class="text-white" href="#">住商不動產</a></li>
				    <li class="breadcrumb-item"><a class="text-white" href="#">永慶房屋</a></li>
                                    <li class="breadcrumb-item"><a class="text-white" href="#">好房網</a></li>
                                    <li class="breadcrumb-item"><a class="text-white" href="#">591租屋網</a></li>
                                    <!--<li class="breadcrumb-item text-white active" aria-current="page">Service</li>-->
                                </ol>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Navbar & Hero End -->


        <!-- Full Screen Search Start -->
        <div class="modal fade" id="searchModal" tabindex="-1">
            <div class="modal-dialog modal-fullscreen">
                <div class="modal-content" style="background: rgba(29, 29, 39, 0.7);">
                    <div class="modal-header border-0">
                        <button type="button" class="btn bg-white btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body d-flex align-items-center justify-content-center">
                        <div class="input-group" style="max-width: 600px;">
                            <input type="text" class="form-control bg-transparent border-light p-3" placeholder="Type search keyword">
                            <button class="btn btn-light px-4"><i class="bi bi-search"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Full Screen Search End -->


	<!-- Service Start -->
	    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            padding: 8px;
            text-align: center;
            border: 1px solid black;
        }

        th {
            background-color: lightgray;
	}
    </style>
        <div class="container-xxl py-5">
            <div class="container px-lg-5">
                <div class="section-title position-relative text-center mb-5 pb-2 wow fadeInUp" data-wow-delay="0.1s">
                    <h6 class="position-relative d-inline text-primary ps-4">爬蟲資料(30筆)</h6>
                    <h2 class="mt-2">新店區-買</h2>
                </div>
                <table >
								<thead>
									<tr>
										<th>district</th>
										<th>age</th>
										<th>square</th>
										<th>square_price</th>
										<th>type</th>
                                        <th>total_price</th>
                                        <th>search</th>
									</tr>
								</thead>
								<tbody> 
								  <?php
                                    while($row = mysqli_fetch_assoc($result)) {
								        ?>
                                            <tr>
											    <td ><?php echo $row["district"];?></td>
												<td ><?php echo $row["age"];?></td>
												<td ><?php echo $row["square"];?></td>
												<td><?php echo $row["square_price"];?></td>
												<td><?php echo $row["type"];?></td>
                                                <td><?php echo $row["total_price"];?></td>
                                                <td><?php echo $row["search"];?></td>
											</tr>  <?php
										} 
								  ?>
								</tbody>								
							</table>
        <div class="container-xxl py-5">
            <div class="container px-lg-5">
                <div class="section-title position-relative text-center mb-5 pb-2 wow fadeInUp" data-wow-delay="0.1s">
                    <h6 class="position-relative d-inline text-primary ps-4">爬蟲資料(30筆)</h6>
                    <h2 class="mt-2">文山區-買</h2>
                </div>
                <table >
								<thead>
									<tr>
										<th>district</th>
										<th>age</th>
										<th>square</th>
										<th>square_price</th>
										<th>type</th>
                                        <th>total_price</th>
                                        <th>search</th>
									</tr>
								</thead>
								<tbody> 
								  <?php
                                    while($row = mysqli_fetch_assoc($result2)) {
								        ?>
                                            <tr>
											    <td ><?php echo $row["district"];?></td>
												<td ><?php echo $row["age"];?></td>
												<td ><?php echo $row["square"];?></td>
												<td><?php echo $row["square_price"];?></td>
												<td><?php echo $row["type"];?></td>
                                                <td><?php echo $row["total_price"];?></td>
                                                <td><?php echo $row["search"];?></td>
											</tr>  <?php
										} 
								  ?>
								</tbody>								
							</table>
        <div class="container-xxl py-5">
            <div class="container px-lg-5">
                <div class="section-title position-relative text-center mb-5 pb-2 wow fadeInUp" data-wow-delay="0.1s">
                    <h6 class="position-relative d-inline text-primary ps-4">爬蟲資料(30筆)</h6>
                    <h2 class="mt-2">新店區-租</h2>
                </div>
                <table >
								<thead>
									<tr>
										<th>district</th>
										<th>age</th>
										<th>square</th>
										<th>square_price</th>
										<th>type</th>
                                        <th>total_price</th>
                                        <th>search-1</th>
                                        <th>search-2</th>
									</tr>
								</thead>
								<tbody> 
								  <?php
                                    while($row = mysqli_fetch_assoc($result3)) {
								        ?>
                                            <tr>
											    <td ><?php echo $row["district"];?></td>
												<td ><?php echo $row["age"];?></td>
												<td ><?php echo $row["square"];?></td>
												<td><?php echo $row["square_price"];?></td>
												<td><?php echo $row["type"];?></td>
                                                <td><?php echo $row["total_price"];?></td>
                                                <td><?php echo $row["search/0"];?></td>
                                                <td><?php echo $row["search/1"];?></td>

											</tr>  <?php
										} 
								  ?>
								</tbody>								
							</table>
        <div class="container-xxl py-5">
            <div class="container px-lg-5">
                <div class="section-title position-relative text-center mb-5 pb-2 wow fadeInUp" data-wow-delay="0.1s">
                    <h6 class="position-relative d-inline text-primary ps-4">爬蟲資料(30筆)</h6>
                    <h2 class="mt-2">文山區-租</h2>
                </div>
                <table >
								<thead>
									<tr>
										<th>district</th>
										<th>age</th>
										<th>square</th>
										<th>square_price</th>
										<th>type</th>
                                        <th>total_price</th>
                                        <th>search-1</th>
                                        <th>search-2</th>
									</tr>
								</thead>
								<tbody> 
								  <?php
                                    while($row = mysqli_fetch_assoc($result4)) {
								        ?>
                                            <tr>
											    <td ><?php echo $row["district"];?></td>
												<td ><?php echo $row["age"];?></td>
												<td ><?php echo $row["square"];?></td>
												<td><?php echo $row["square_price"];?></td>
												<td><?php echo $row["type"];?></td>
                                                <td><?php echo $row["total_price"];?></td>
                                                <td><?php echo $row["search/0"];?></td>
                                                <td><?php echo $row["search/1"];?></td>
											</tr>  <?php
										} 
								  ?>
								</tbody>								
							</table>
            </div>
        </div>
        <!-- Service End -->

        <!-- Back to Top -->
        <a href="#" class="btn btn-lg btn-primary btn-lg-square back-to-top pt-2"><i class="bi bi-arrow-up"></i></a>
    </div>

    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="lib/wow/wow.min.js"></script>
    <script src="lib/easing/easing.min.js"></script>
    <script src="lib/waypoints/waypoints.min.js"></script>
    <script src="lib/owlcarousel/owl.carousel.min.js"></script>
    <script src="lib/isotope/isotope.pkgd.min.js"></script>
    <script src="lib/lightbox/js/lightbox.min.js"></script>

    <!-- Template Javascript -->
    <script src="js/main.js"></script>
</body>

</html>
