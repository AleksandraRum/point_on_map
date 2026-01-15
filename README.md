# Backend-приложение на Django для работы с гео-точками
### backend-приложение на Django для работы с географическими точками на карте. Приложение предоставляет REST API для создания точек, обмена сообщениями и поиска контента в заданном радиусе от указанных координат.

## Стек технологий:
* Python
* Django
* Django REST Framework
* PostgreSQL + PostGIS
* Docker Compose
* Django APITestCase


## Запустить проект:

### 1. Клонировать проект:

```
git clone git@github.com:AleksandraRum/point_on_map.git
cd point_on_map
```

### 2. Установить зависимости:

```pip install -r requirements.txt```

### 3. Запустить базу данных в контейнере:

```docker compose up -d```

### 4. Применить миграции:

```python manage.py migrate```

### 5. Запустить сервер

```python manage.py runserver```

### 5. Создать суперюзера:

```python manage.py createsuperuser```

### 6. Создать токен:
#### В проекте используется TokenAuthentication

- Отправить запрос на эндпоинт:

```POST /auth/token/```

```
"username": "your_username"
"password": "your_password"
```

- Ответ:

``` "token": "your_token"```

- Во всех эндпоинтах необходимо передавать токен в заголовке:

```Authorization: Token your_token```

## Эндпоинты

### 1. Создание точки на карте:
- Эндпоинт:

```POST /api/points/```

- Тело запроса:

```json
{
  "latitude": 41.3888,
  "longitude": 2.15899
}
```

### 2. Создание сообщения к заданной точке:

- Эндпоинт:

```POST /api/points/messages/```

- Тело запроса:

```json
{
  "text": "Hello",
  "point": 1
}
```

### 3. Поиск точек в заданном радиусе:

- Эндпоинт:

```GET /api/points/search/?latitude=...&longitude=...&radius=...```

### 4. Получение сообщений от пользователей в заданной области / радиусе:

- Эндпоинт:

```GET /api/points/messages/search/?latitude=...&longitude=...&radius=...```

## Тестирование

В проекте реализованы тесты с использованием Django APITestCase, покрывающие:
-	создание точек,
-	создание сообщений,
-	поиск точек по радиусу,
-	поиск сообщений по радиусу,
-	проверки аутентификации и валидации входных данных.

### Запуск тестов:

```python manage.py test```



















