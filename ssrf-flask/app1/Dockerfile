FROM python:3.9-slim

# Создаем непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY app1/requirements.txt .
RUN pip install -r requirements.txt

COPY app1/app.py .

# Меняем владельца файлов
RUN chown -R appuser:appuser /app

# Переключаемся на непривилегированного пользователя
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:7000", "app:app"]
