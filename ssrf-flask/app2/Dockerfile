FROM python:3.9-slim

# Обновляем систему и устанавливаем tini
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Создаем непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY app2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app2/app.py .

# Меняем владельца файлов
RUN chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["gunicorn", "--bind", "0.0.0.0:7001", "--workers", "3", "--timeout", "30", "app:app"]
