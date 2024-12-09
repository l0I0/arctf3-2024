<?php
define('DB_HOST', 'sqli-form-mysql');
define('DB_NAME', 'myapp');
define('DB_USER', 'user');
define('DB_PASS', 'password');

try {
    $pdo = new PDO(
        "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4",
        DB_USER,
        DB_PASS,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        ]
    );
} catch(PDOException $e) {
    error_log("Database connection failed: " . $e->getMessage());
    die("Сервис временно недоступен");
}

session_start([
    'cookie_httponly' => true,
    'cookie_secure' => false,
    'cookie_samesite' => 'Lax',
    'cookie_path' => '/',
    'cookie_domain' => '',
    'cookie_lifetime' => 86400
]); 