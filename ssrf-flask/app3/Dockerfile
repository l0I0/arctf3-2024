# Используем официальный образ Python
FROM python:3.9-slim

# Обновляем систему и устанавливаем необходимые пакеты
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Создаем непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей
COPY app3/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY app3/ .

# Создаем директории для загрузки и устанавливаем права
RUN mkdir -p /app/uploads /app/images && \
    chown -R appuser:appuser /app

USER appuser

# Указываем порт, который будет использовать приложение
EXPOSE 7002

# Запускаем приложение
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "app.py"]