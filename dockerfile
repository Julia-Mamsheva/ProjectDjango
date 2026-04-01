FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Собираем статику при сборке образа
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "projectDjango.wsgi:application", "--bind", "0.0.0.0:8080"]