<?php session_start() ?>
<?php
if (isset($_POST['id_prac']) &&
 is_numeric($_POST['id_prac']) &&
 is_string($_POST['nazwisko']))
 {
      $link = mysqli_connect("localhost", "scott", "tiger", "instytut");
      if (!$link) {
          printf("Connect failed: %s\n", mysqli_connect_error());
          exit();
      }
     $sql = "INSERT INTO pracownicy(id_prac,nazwisko) VALUES(?,?)";
     $stmt = $link->prepare($sql);
     $stmt->bind_param("is", $_POST['id_prac'], $_POST['nazwisko']);
     $result = $stmt->execute();
     $_SESSION["feedback"] = 1;
     if (!$result) {
        header("Location: file06_post.php");
     } else {
        header("Location: file06_get.php");
     }
     $stmt->close();
     $result->free();
     $link->close();
 }
?>
