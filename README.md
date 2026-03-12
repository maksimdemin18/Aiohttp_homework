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
<img width="1353" height="1143" alt="Screenshot_20260312_122527" src="https://github.com/user-attachments/assets/4165cfb4-cd8c-4ec8-b098-5e0bfa8030e9" />

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
<img width="1563" height="195" alt="Screenshot_20260312_135113" src="https://github.com/user-attachments/assets/45301bf4-1dd7-455e-9ebf-a425b180a0fa" />

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
<img width="981" height="200" alt="Screenshot_20260312_135141" src="https://github.com/user-attachments/assets/b0b7279a-9ccb-4114-846c-9c7cc1e4a2cf" />

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
<img width="1727" height="204" alt="Screenshot_20260312_135446" src="https://github.com/user-attachments/assets/5361687d-aa20-4ff4-9631-0d9a5caebbf7" />


5. Получение объявления 
```
curl http://127.0.0.1:8080/ads/1
```
<img width="1707" height="75" alt="Screenshot_20260312_135527" src="https://github.com/user-attachments/assets/68979f95-cca4-48da-990c-1e84d1618aad" />


6. Редактирование объявления 
```
curl -X PATCH http://127.0.0.1:8080/ads/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN>" \
-d '{
"title": "Продам ноутбук срочно"
}'
```
<img width="1707" height="202" alt="Screenshot_20260312_135623" src="https://github.com/user-attachments/assets/effa309d-d883-4c98-9c62-7a3e28f6782a" />


7. Удаление объявления 
```
curl -X DELETE http://127.0.0.1:8080/ads/1 \
-H "Authorization: Bearer <TOKEN>"
```
<img width="993" height="73" alt="Screenshot_20260312_135658" src="https://github.com/user-attachments/assets/44997ba6-6a54-48c2-b402-fe8f53bc7b4b" />


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
