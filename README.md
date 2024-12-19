
# **Habit Tracker API**

## Описание

Habit Tracker — это приложение для управления и отслеживания полезных привычек. Оно позволяет пользователям создавать, редактировать, удалять и просматривать привычки. Также интеграция с Telegram обеспечивает удобные напоминания.

Этот проект реализован с использованием Django REST Framework и PostgreSQL, поддерживает фоновые задачи через Celery и Redis, а также включает документацию API с помощью Swagger.

---

## Функциональные возможности

- Регистрация и авторизация пользователей.
- Создание и управление привычками.
- Публичный доступ к привычкам других пользователей.
- Интеграция с Telegram для напоминаний.
- Поддержка пагинации.
- Валидаторы для проверки корректности данных.
- Отложенные задачи через Celery.
- Документация API с помощью Swagger.

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/habit-tracker.git
cd habit-tracker
```

### 2. Настройка виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```plaintext
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=habit_tracker
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен по адресу [http://localhost:8000](http://localhost:8000).

---

## Использование Docker

1. Соберите образ Docker:
   ```bash
   docker-compose up --build
   ```

2. Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000).

---

## Документация API

Документация доступна по адресу:
- Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## Тестирование

### 1. Запуск тестов:

```bash
pytest
```

### 2. Генерация покрытия тестами:

```bash
pytest --cov=habits
```

---

## Основные технологии

- **Backend**: Django, Django REST Framework
- **База данных**: PostgreSQL
- **Фоновые задачи**: Celery, Redis
- **API-документация**: Swagger (drf-yasg)
- **Контейнеризация**: Docker, Docker Compose
- **Тестирование**: Pytest



---

## Лицензия

Этот проект находится под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

---

## Дополнительно

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной или создайте issue в репозитории.
