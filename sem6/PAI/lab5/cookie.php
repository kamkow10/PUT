<?php session_start(); ?>
<!DOCTYPE html>
<html>
    <head>
        <title>PHP</title>
        <meta charset='UTF-8' />
    </head>
    <body>
        <a href="index.php">Wstecz</a>
        <?php
            require_once("funkcje.php");
            if (isSet($_GET["utworzCookie"])) {
                setcookie("cookie", "cookieValue", time() + $_GET["czas"], "/");
                echo "Utworzono cookie ! :D";
            }
        ?>
    </body>
</html>
