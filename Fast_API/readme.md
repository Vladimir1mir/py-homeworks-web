#### Запуск:

1. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Используйте docker-compose для запуска контейнера:
```bash
docker-compose up -d
```

3. Выполнять запросы можно c помощью Swagger `http://localhost:8000/docs/`, `requests-examples.http` или `client.py`

Вы можете использовать HTTP-запросы с помощью расширения для вашего редактора кода (например, VSCode) или через инструмент requests для тестирования серверных API.


# Домашнее задание к лекции «Создание REST API на FastApi» часть 1

Инструкцию по сдаче домашнего задания Вы найдете на главной странице репозитория.

# Задание 
Вам нужно написать на fastapi и докеризировать сервис объявлений купли/продажи.

У объявлений должны быть следующие поля:
 - заголовок
 - описание
 - цена
 - автор
 - дата создания

Должны быть реализованы следующе методы:
 - Создание: `POST /advertisement`
 - Обновление: `PATCH /advertisement/{advertisement_id}`
 - Удаление: `DELETE /advertisement/{advertisement_id}`
 - Получение по id: `GET  /advertisement/{advertisement_id}`
 - Поиск по полям: `GET /advertisement?{query_string}`

Авторизацию и аутентификацию реализовывать **не нужно**