#!/bin/bash
set -e

# Ждем, пока MySQL станет доступен
until php -r "
try {
    \$dbh = new PDO('mysql:host=sqli-form-;dbname=myapp', 'user', 'password');
    echo 'MySQL подключен успешно\n';
    exit(0);
} catch(PDOException \$e) {
    echo 'Ожидание MySQL...\n';
    exit(1);
}
"
do
    sleep 1
done

# Запускаем скрипт инициализации
php /var/www/html/init_user.php

# Запускаем Apache в фоновом режиме
exec "$@" 