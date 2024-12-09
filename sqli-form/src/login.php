<?php
require_once 'config.php';

$error = '';
error_log("Current User-Agent: " . $_SERVER['HTTP_USER_AGENT']);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    $query = "SELECT id, username, password, useragent FROM users WHERE username = '$username'";
    $result = $pdo->query($query);
    
    $user = $result->fetch();
    if ($user && $user['username'] === 'admin' && $user['password'] === md5($password)) {
        if (!empty($user['useragent']) && $user['useragent'] !== $_SERVER['HTTP_USER_AGENT']) {
            $error = 'Обнаружен вход с неизвестного устройства. Доступ запрещен!';
        } else {
            $_SESSION['user_id'] = $user['id'];
            header('Location: index.php');
            exit();
        }
    } else {
        $error = 'Неверное имя пользователя или пароль';
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Вход</title>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <canvas id="starfield"></canvas>
    <div class="container">
        <h1>Вход в систему</h1>
        <?php if ($error): ?>
            <div class="error"><?php echo $error; ?></div>
        <?php endif; ?>
        <form method="POST" action="login.php">
            <div class="form-group">
                <label>Имя пользователя:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Пароль:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn">Войти</button>
        </form>
    </div>
    <script src="starfield.js"></script>
</body>
</html> 