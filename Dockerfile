FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production

# Most PaaS providers will inject PORT; fall back to 5000
ENV PORT=5000

EXPOSE 5000

CMD gunicorn wsgi:app --bind 0.0.0.0:${PORT}

