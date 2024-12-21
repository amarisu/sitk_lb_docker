FROM python:3.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

RUN apk update && \
    apk add --no-cache gcc musl-dev postgresql-dev postgresql-client

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entry.sh
RUN chown -R appuser:appgroup /app

USER appuser

RUN pip cache purge

ENTRYPOINT ["./entry.sh"]
CMD ["flask", "run", "--host=0.0.0.0"]
