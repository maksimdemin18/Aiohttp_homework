# Домашнее задание к занятию "`Aiohttp`" - `Дёмин Максим`


### Задание 1

Что нужно сделать:

Переписать сервис из домашнего задания по Flask на aiohttp.

Результатом работы является API, написанный на aiohttp.

### Решение:

Установка и запуск локально 
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Сервер будет доступен по адресу: 
```
http://127.0.0.1:8080
```

Проверка работы API 
1. Проверка health-check 
```
curl http://127.0.0.1:8080/health
```

2. Регистрация пользователя 
```
curl -X POST http://127.0.0.1:8080/users \
-H "Content-Type: application/json" \
-d '{
"email": "student@example.com",
"password": "123456"
}'
```

3. Авторизация и получение токена 
```
curl -X POST http://127.0.0.1:8080/login \
-H "Content-Type: application/json"
-d '{
"email": "student@example.com",
"password": "123456"
}'
```

Пример ответа: 
```
{
"token":"<TOKEN>"
}
```
4. Создание объявления 
```
curl -X POST http://127.0.0.1:8080/ads \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN>" \
-d '{
"title": "Продам ноутбук",
"description": "Ноутбук в хорошем состоянии"
}'
```
5. Получение объявления 
```
curl http://127.0.0.1:8080/ads/1
```
6. Редактирование объявления 
```
curl -X PATCH http://127.0.0.1:8080/ads/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN>" \
-d '{
"title": "Продам ноутбук срочно"
}'
```
7. Удаление объявления 
```
curl -X DELETE http://127.0.0.1:8080/ads/1 \
-H "Authorization: Bearer <TOKEN>"
```
### Задание 2

Что нужно сделать:

Докеризировать API, написанный в задании 1.
Чтобы проверить корректность работы сервиса, нужно:

запустить контейнер
проверить работу роута

### Решение:

Через Docker 
```
docker build -t aiohttp-ads-api .
docker run -p 8080:8080 aiohttp-ads-api
```
Через Docker Compose 
```
docker compose up --build
```
