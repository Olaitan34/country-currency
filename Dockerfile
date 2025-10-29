# Dockerfile for Sevalla deployment
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app directory
WORKDIR /app

# Install system dependencies for mysqlclient/pymysql
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create cache directory for summary images
RUN mkdir -p cache && chmod 755 cache

# Make start.sh executable
RUN chmod +x start.sh

# Expose port (Sevalla will assign via PORT env var)
EXPOSE 8080

# Run startup script
CMD ["/bin/sh", "start.sh"]
