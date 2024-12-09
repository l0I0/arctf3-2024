# Базовый образ с Python
FROM python:3.11-slim AS python-base

# Установка рабочего каталога
WORKDIR /hippo/

# Установка основных переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Этап сборки зависимостей
FROM python-base AS build

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /hippo/
RUN pip install --no-cache-dir -r requirements.txt

# Этап сборки приложения
FROM python-base AS development

WORKDIR /hippo/app
# Настройка рабочего пользователя
RUN groupadd -g 1500 hippo && \
    useradd -m -u 1500 -g hippo hippo

# Переключение на пользователя hippo
USER hippo

# Копирование зависимостей из этапа сборки
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Копируем исходный код приложения
COPY --chown=hippo . .

# Команда запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]