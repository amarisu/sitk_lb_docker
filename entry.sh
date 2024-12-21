#!/bin/sh

echo "Все переменные окружения:"
env

# Ждем, пока база данных будет доступна
until pg_isready -h db -p 5432; do
  echo "Ждем, пока база данных будет доступна..."
  sleep 2
done

: "${DATABASE_URL:?DATABASE_URL не установлена}"
: "${FLASK_APP:?FLASK_APP не установлена}"

# Инициализируем миграции, если папка migrations не существует
if [ ! -d "migrations" ]; then
    echo "Инициализация миграций..."
    flask db init
    flask db migrate -m "Initial migration"
fi

flask db upgrade  
exec "$@"
