# Base image
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=sokoban_backend.settings

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    default-mysql-client \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
# RUN python manage.py collectstatic --noinput --clear

# Expose ports
EXPOSE 8050

# Run application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "sokoban_backend.wsgi"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8050"]