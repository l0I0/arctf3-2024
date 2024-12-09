CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    useragent VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Добавляем тестового пользователя
INSERT INTO users (username, password, salt, useragent) VALUES 
('admin', MD5('mau1992jalisco09'), '', 'Mozilla/5.0 (Vulcan/9.6; ChronosOS 42.0) Gecko/4.3 (Alpha Centauri-Protocol/0.1) Quantum/98.76.54 Mobile/Hoverboard-Beta UA/Undefined-AI-9000');