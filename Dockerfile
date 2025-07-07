# ---------- client build stage ----------
FROM node:20 AS client-build
WORKDIR /app

# Copy only the Svelte client source
COPY client/ ./client
WORKDIR /app/client

# Install and build Svelte assets
RUN npm install --legacy-peer-deps ; npm run build

# ---------- python runtime stage ----------
FROM python:3.11-slim AS runtime
WORKDIR /srv

ENV DJANGO_SETTINGS_MODULE=config.settings

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY . /srv

# Copy built static assets from previous stage
COPY --from=client-build /app/static/ /srv/static/

# Prepare static root and collect static files
RUN mkdir -p /srv/staticfiles && \
    python manage.py collectstatic --noinput -v 0

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application 