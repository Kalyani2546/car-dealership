FROM node:22-alpine AS frontend-build
WORKDIR /build
COPY frontend/client/package*.json ./
RUN npm ci
COPY frontend/client/ ./
RUN npm run build

FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DJANGO_DEBUG=0
WORKDIR /app
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt
COPY server/ /app/server/
COPY --from=frontend-build /build/dist/ /app/frontend/client/dist/
WORKDIR /app/server
RUN DJANGO_DEBUG=1 DJANGO_SECRET_KEY=collectstatic-build-only python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_dealerships && gunicorn dealership_project.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
