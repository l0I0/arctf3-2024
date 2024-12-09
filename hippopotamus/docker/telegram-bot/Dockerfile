FROM python:3.11-slim

WORKDIR /bot

# Установка только необходимых зависимостей
COPY ./telegram-bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем непривилегированного пользователя
RUN useradd -m botuser && \
    chown -R botuser:botuser /bot

USER botuser

# Запускаем runner.py вместо main.py
CMD ["python", "runner.py"]