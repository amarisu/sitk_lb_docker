# Лабораторная работа: Docker - Докеризация приложения

Данный проект представляет собой Flask-приложение, которое использует PostgreSQL в качестве базы данных. В проекте используются миграции для автоматического обновления структуры базы данных при запуске контейнера. Все конфигурационные параметры (например, данные для подключения к базе данных) задаются через переменные окружения. Для хранения зависимостей используется внешний том Docker.

Выполнили: Колногорова Александра, Ананьевский Иван (гр. 2300)

## Запуск проекта

1. Запуск контейнеров:

```bash
docker-compose up --build
```
2. Проверка работоспособности приложения (пример для Windows):

```bash
### Создание пользователя
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d "{\"username\": \"testuser\"}"

### Получение списка пользователей
curl http://localhost:5000/users

### Создание задачи для пользователя
curl -X POST http://localhost:5000/users/{user_id}/tasks -H "Content-Type: application/json" -d "{\"description\": \"Тестовая задача\"}"

### Получение списка задач пользователя
curl http://localhost:5000/users/{user_id}/tasks
 
### Обновление статуса задачи
curl -X PUT http://localhost:5000/tasks/{task_id} -H "Content-Type: application/json" -d "{\"completed\": true}"

### Удаление задачи
curl -X DELETE http://localhost:5000/tasks/{task_id}
```

