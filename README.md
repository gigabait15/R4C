# Django Robot Management System

**Проект для управления данными о роботах, их заказами, а также генерации отчетов по производству роботов. Включает в себя несколько функций:**

- API для добавления роботов.
- Генерация Excel отчета по производству роботов.
- Отправка уведомлений клиентам, когда заказанный робот возвращается в наличие.
---
### Структура проекта

```
/robot-management/
│
├── customers                          # Приложение для работы с клиентами
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── db.sqlite3                         # База данных (SQLite)
├── LICENSE                            # Лицензия проекта
├── manage.py                          # Скрипт для управления проектом
├── media                              # Директория для хранения медиа файлов 
├── orders                             # Приложение для управления заказами
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py
│   ├── tasks.py
│   ├── templates/
│   │   └── orders/
│   │       ├── order_create.html
│   │       └── order_list.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── R4C                                # Основная директория проекта, включая настройки
│   ├── asgi.py                        # Настройки ASGI для проекта
│   ├── celery.py                      # Настройки Celery для асинхронных задач
│   ├── __init__.py
│   ├── settings.py                    # Основные настройки Django проекта
│   ├── urls.py                        # Основные маршруты проекта
│   └── wsgi.py                        # Настройки WSGI для проекта
├── README.md                          # Основной файл документации проекта
├── req.txt                            # Файл с зависимостями проекта
├── robots                             # Приложение для работы с роботами
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── management/
│   │   └── commands/
│   │       ├── db_conn.py             # Команда для заполнения БД фиксурами
│   │       ├── get_weekly_report.py   # Команда для получения еженедельного отчета
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   │   └── robots/
│   │       ├── download_weekly_report.html
│   │       ├── list_robots.html
│   │       └── robots_create.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── task_description                    # Описание задач и документация к тз
    ├── README.md
    └── tasks.md
```
---
### Установка и настройка
#### 1. Клонирование репозитория
Клонируйте репозиторий:
```
git clone https://github.com/gigabait15/R4C.git
```

#### 2. Установка зависимостей
Создайте виртуальное окружение и установите все зависимости:
```
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate     # Для Windows
pip install -r req.txt
```
#### 3. Настройка базы данных
Настройте базу данных в settings.py. По умолчанию настройки для БД SQlite3

#### 4. Выполнение миграций
Примените миграции для создания таблиц в базе данных:
```
python manage.py makemigrations
python manage.py migrate
```

#### 5. Запуск сервера
Запустите сервер Redis и Django:
```
redis-server
python manage.py runserver
```
Теперь проект будет доступен по адресу http://localhost:8000.

#### 6. Настройка отправки электронной почты
Для отправки уведомлений настройте параметры SMTP сервера в settings.py:
````
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_password'
````
---

