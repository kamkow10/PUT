<?php session_start() ?>
<html>
<body>
    <div>
    <a href="file06_post.php">POST</a>
    </div>
    <?php if ($_SESSION["feedback"] == 1) { ?>
    <div style="color: green">Udało się zalogować!</div>
    <?php
    $_SESSION["feedback"] = 0;
    }?>
</body>
<?php
$link = mysqli_connect("localhost", "scott", "tiger", "instytut");
if (!$link) {
     printf("Connect failed: %s\n", mysqli_connect_error());
     exit();
}
$sql = "SELECT * FROM pracownicy";
$result = $link->query($sql);
foreach ($result as $v) {
    echo $v["ID_PRAC"]." ".$v["NAZWISKO"]."<br/>";
}
$result->free();
$link->close();
?>
