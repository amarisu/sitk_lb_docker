# Стадия сборки
FROM python:3.11-alpine AS builder

WORKDIR /app

RUN apk update && \
    apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Финальная стадия
FROM python:3.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Устанавливаем только необходимые runtime-зависимости
RUN apk add --no-cache postgresql-client libpq

# Копируем установленные пакеты из стадии сборки
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .

RUN chmod +x entry.sh
RUN chown -R appuser:appgroup /app

USER appuser

ENTRYPOINT ["./entry.sh"]
CMD ["flask", "run", "--host=0.0.0.0"]