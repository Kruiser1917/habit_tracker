# Базовый образ
FROM python:3.10

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта
COPY . .

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Открытие порта
EXPOSE 8000

# Запуск сервера разработки
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
