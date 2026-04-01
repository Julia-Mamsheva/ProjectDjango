FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаём папку заранее и собираем статику
RUN mkdir -p /app/staticfiles /app/static && \
    DJANGO_SECRET_KEY=build-dummy-key python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && gunicorn projectDjango.wsgi:application --bind 0.0.0.0:8080"]