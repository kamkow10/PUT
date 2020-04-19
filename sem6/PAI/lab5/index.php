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
        <h1>Nasz system</h1>
        <div>
            <?php
                if (isSet($_COOKIE["cookie"])) {
                    echo $_COOKIE["cookie"];
                } else {
                    echo "Nie ma cookie :(";
                }
            ?>
        </div>
        <a href="index.php">Index</a>
        <a href="user.php">User</a>
        <form action="logowanie.php" method="POST">
            <fieldset>
                <legend>Logowanie</legend>
                <div>
                    <label for="login">Login</label>
                    <input name="login" type="text"/>
                </div>
                <div>
                    <label for="haslo">Hasło</label>
                    <input name="haslo" type="password"/>
                </div>
                <div>
                    <input name="zaloguj" type="submit" value="Zaloguj"/>
                </div>
            </fieldset>
        </form>
        <form action="cookie.php" method="GET">
            <fieldset>
                <legend>Ustawianie cookie (w sekundach)</legend>
                <input type="number" name="czas"/>
                <input type="submit" name="utworzCookie" value="Utwórz cookie"/>
            </fieldset>
        </form>
    </body>
</html>
<?php
    if (isSet($_POST["wyloguj"])) {
        $_SESSION["zalogowany"] = 0;
    }
    if (isSet($_POST["submitSendingFile"])) {
        $cwd = getCwd();
        $newDir = "/obrazy/";
        $filename = $_FILES["sendFile"]["name"];
        $filesize = $_FILES["sendFile"]["size"];
        $fileTmpName = $_FILES["sendFile"]["tmp_name"];
        $fileType = $_FILES["sendFile"]["type"];
        echo $fileType;
        if(($filename != "") and
        (
        ($fileType == "image/png") or ($fileType == "image/jpg") or
        ($fileType == "image/jpeg") or ($fileType == "image/PNG")
        )) {
            $newPath = $cwd . $newDir . $filename;
            if (move_uploaded_file($fileTmpName, $newPath)) {
                echo "Zdjećie załadowane!";
            } else {
                echo "Zdjećie nie załadowane!";
            }
        } else {
            echo "Zły plik!";
        }
    }
?>
