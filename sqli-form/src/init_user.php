<?php
require_once 'config.php';

function createDefaultUser($pdo) {
    // Специальный User-Agent
    $special_ua = "Mozilla/5.0 (Vulcan/9.6; ChronosOS 42.0; RV:∞) Gecko/4.3 (Alpha Centauri-Protocol/0.1) Quantum/98.76.54 Mobile/Hoverboard-Beta UA/Undefined-AI-9000";
    
    // Проверяем существует ли пользователь admin
    $stmt = $pdo->prepare("SELECT id FROM users WHERE username = 'admin'");
    $stmt->execute();
    
    if (!$stmt->fetch()) {
        // Создаем пользователя с заданным User-Agent
        $query = "INSERT INTO users (username, password, salt, useragent) VALUES 
                 ('admin', MD5('mau1992jalisco09'), '', '$special_ua')";
        $pdo->query($query);
        echo "Пользователь admin создан успешно с специальным User-Agent\n";
    } else {
        // Обновляем User-Agent для существующего пользователя
        $query = "UPDATE users SET useragent = '$special_ua' WHERE username = 'admin'";
        $pdo->query($query);
        echo "User-Agent обновлен для существующего пользователя admin\n";
    }
}

try {
    // Создаем таблицу если она не существует
    $sql = "CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(32) NOT NULL,
        salt VARCHAR(32) NOT NULL,
        useragent VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )";
    
    $pdo->exec($sql);
    echo "Таблица users проверена/создана\n";
    
    // Создаем пользователя
    createDefaultUser($pdo);
    
} catch(PDOException $e) {
    die("Ошибка: " . $e->getMessage() . "\n");
} 