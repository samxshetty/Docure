<?php
#Database connection
$servername = "localhost";
$username = "root";
$password = "";
$database = "innovixlabs";

$conn = new mysqli($servername, $username, $password, $database);

#Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

#Sign-in logic
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if(empty($_POST['email']) || empty($_POST['password'])) {
        echo "<script>
                alert('Error: Please enter both email and password.');
                window.location.href = 'index.html';
              </script>";
        exit; 
    }
    
    $email = $_POST['email'];
    $password = $_POST['password'];

    $email = mysqli_real_escape_string($conn, $email);
    $password = mysqli_real_escape_string($conn, $password);

    $sql = "SELECT * FROM users WHERE email='$email'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        #Email exists, check password
        $row = $result->fetch_assoc();
        if ($row['password'] === $password) {
            #Password matches, display welcome image and redirect
            echo "<img src='Welcome Back.png' alt='Welcome Image' id='welcome-image'>";
            echo "<script>
                    setTimeout(function(){
                        window.location.href = 'https://samridhshetty.my.canva.site/innovix-labs';
                    }, 4000);
                  </script>";
        } else {
            #Incorrect password, redirect to main page with popup
            echo "<script>
                    alert('Incorrect password');
                    window.location.href = 'index.html';
                  </script>";
        }
    } else {
        #Email doesn't exist, create new user
        $sql = "INSERT INTO users (email, password) VALUES ('$email', '$password')";
        if ($conn->query($sql) === TRUE) {
            #New user created successfully, display welcome new user image and redirect
            echo "<img src='Welcome New.png' alt='Welcome New User Image' id='welcome-new-user-image'>";
            echo "<script>
                    setTimeout(function(){
                        window.location.href = 'https://samridhshetty.my.canva.site/innovix-labs';
                    }, 4000);
                  </script>";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    }
}
$conn->close();
