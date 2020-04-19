<?php
    session_start();
?>
<!DOCTYPE html>
<html>
    <head>
        <title>PHP</title>
        <meta charset='UTF-8' />
    </head>
    <body>
        <?php
            require_once("funkcje.php");
            if ($_SESSION["zalogowany"] == 0) {
                header("Location: index.php");
            } else {
                echo "Zalogowano jako:" . $_SESSION["zalogowanyImie"] ;
            }
        ?>
        <div>
            <a href="index.php">Index</a>
            <a href="user.php">User</a>
        </div>
        <?php if(file_exists("obrazy/bocian.jpg")) { echo "tak"; ?>
            <img src="obrazy/bocian.jpg"/>
        <?php } else { echo "nie"; ?>
            <div style="border: 1px solid; padding: 5px; width: 200px">
                Brak obrazka :(
            </div>
        <?php } ?>
        <form action="index.php" method="POST">
            <fieldset>
                <legend>Wylogowanie</legend>
                <input type="submit" name="wyloguj" value="wyloguj"/>
            </fieldset>
        </form>
        <form action='index.php' method='POST' enctype='multipart/form-data'>
            <fieldset>
                <legend>Prześlij obrazek</legend>
                <input name="sendFile" type="file"/>
                <input type="submit" name="submitSendingFile"/>
            </fieldset>
        </form>
    </body>
</html>
