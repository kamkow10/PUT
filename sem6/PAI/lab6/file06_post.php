<?php session_start() ?>
<?php
 $link = mysqli_connect("localhost", "scott", "tiger", "instytut");
 if (!$link) {
     printf("Connect failed: %s\n", mysqli_connect_error());
     exit();
 } ?>
 <html>
 <head>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
 </head>
 <body>
 <a href="file06_get.php">GET</a>
 <?php if ($_SESSION["feedback"] == 1) { ?>
     <div style="color: red">Nie udało się zalogować!</div>
 <?php $_SESSION["feedback"] = 0; } ?>
 <form action="file06_redirect.php" method="POST">
     id_prac <input type="text" name="id_prac">
     nazwisko <input type="text" name="nazwisko">
     <input type="submit" value="Wstaw">
     <input type="reset" value="Wyczysc">
 </form>
