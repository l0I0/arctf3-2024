FROM php:8.2-apache

# Устанавливаем только необходимые расширения
RUN docker-php-ext-install -j$(nproc) pdo pdo_mysql

# Включаем mod_rewrite и очищаем кэш
RUN a2enmod rewrite && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем конфигурацию PHP
COPY php.ini /usr/local/etc/php/

WORKDIR /var/www/html

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["apache2-foreground"]