FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY pyproject.toml .

ENV PYTHONUNBUFFERED=1 \
    SENTINEL_HOST=0.0.0.0 \
    SENTINEL_PORT=8080

EXPOSE 8080

CMD ["python", "-m", "app.main"]
