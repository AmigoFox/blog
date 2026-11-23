# Blog

Учебный блог на Django: записи читают все, создавать и редактировать могут только авторизованные пользователи, редактирование — только своих записей. Оформление на Bootstrap 4.

## Возможности

- Регистрация, вход, выход (POST-форма с CSRF)
- Публичная лента записей, новые сверху
- Создание и редактирование публикаций (только автор)
- Админка с поиском и фильтрами
- 11 автоматических тестов

## Локальный запуск

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Открыть http://127.0.0.1:8000/

## Запуск через Docker

```bash
docker compose up -d --build
```

Приложение будет на порту из переменной APP_PORT (по умолчанию 8000).

## Деплой на учебный сервер

1. `ssh student@192.168.1.11` (из сети колледжа, VPN выключен)
2. `newproject <фамилия>-blog` — команда выдаст папку и диапазон портов
3. `cd ~/projects/<фамилия>-blog`
4. `git init -q`
5. `git remote add origin https://github.com/AmigoFox/blog.git`
6. `git pull origin HEAD`
7. `nano .env` — добавить строки ниже, заменив ПОРТ на первый порт своего диапазона:

```dotenv
DJANGO_SECRET_KEY=длинный-уникальный-ключ
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=192.168.1.11,localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://192.168.1.11:ПОРТ
DJANGO_USE_HTTPS=False
SQLITE_PATH=/app/data/db.sqlite3
APP_BIND_IP=0.0.0.0
APP_PORT=ПОРТ
```

8. `docker compose up -d --build`
9. `docker compose exec web python manage.py createsuperuser`
10. Открыть `http://192.168.1.11:ПОРТ/`

Обновление после правок: локально commit+push, на сервере `git pull origin HEAD` и `docker compose up -d --build`.

## Переменные окружения

| Переменная | Назначение |
|---|---|
| DJANGO_SECRET_KEY | секретный ключ Django |
| DJANGO_DEBUG | режим отладки (False на сервере) |
| DJANGO_ALLOWED_HOSTS | разрешённые хосты через запятую |
| DJANGO_CSRF_TRUSTED_ORIGINS | origins для CSRF: адрес с портом или https-домен |
| DJANGO_USE_HTTPS | True при работе за HTTPS-шлюзом преподавателя |
| SQLITE_PATH | путь к файлу базы (на сервере — volume /app/data) |
| APP_BIND_IP | адрес публикации контейнера (0.0.0.0) |
| APP_PORT | внешний порт проекта (первый порт диапазона newproject) |

## Тесты

```bash
python manage.py test
```