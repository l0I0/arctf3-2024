<?php
require_once 'config.php';

// Проверяем авторизацию
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

$stmt = $pdo->prepare("SELECT username FROM users WHERE id = ?");
$stmt->execute([$_SESSION['user_id']]);
$user = $stmt->fetch();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Главная страница</title>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <canvas id="starfield"></canvas>
    <div class="container">
        <h1>Добро пожаловать, <?php echo htmlspecialchars($user['username']); ?>!</h1>
        <div class="flag">
            arctf{r1ckroll-brute}
        </div>
        <a href="logout.php" class="btn">Выйти</a>
    </div>
    <script src="starfield.js"></script>
</body>
</html> 