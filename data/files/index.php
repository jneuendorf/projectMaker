<?php
session_start();
include_once("includes/functions.php");

if (isset($_REQUEST['page'])) {
    $page = $_REQUEST['page'];
    if (!logged_in() && !in_array($page, array("home", "kontakt", "impressum"))) {
        $page = "home";
    }
}
else {
    $page = "home";
}
?>

<html>
<?php include("views/head.php"); ?>
<body>
    <header class="top">
        <?php include("views/header.php"); ?>
    </header>
    <!-- TODO: main tag not supported in IE (any version!)...but header tag is -.- -->
    <main>
        <header>
            <?php include("views/image_slider.php"); ?>
        </header>
        <main class='content'>
            <?php
            if (file_exists("views/$page.php")) {
                include("views/$page.php");
            }
            else {
                include("views/home.php");
            }
            ?>
        </main>
    </main>
</body>
</html>
