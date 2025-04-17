# Base image
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=sokoban_backend.settings \
    # MYSQL_ROOT_PASSWORD=your_root_password \
    # MYSQL_DATABASE=sokoban_db \
    # MYSQL_USER=django_user \
    # MYSQL_PASSWORD=your_password

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose ports
EXPOSE 8000
EXPOSE 3306

# Setup entrypoint
# COPY docker-entrypoint.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/docker-entrypoint.sh
# ENTRYPOINT ["docker-entrypoint.sh"]

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "sokoban_backend.wsgi"]