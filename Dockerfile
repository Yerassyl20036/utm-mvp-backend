# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copy application code
COPY . .

# Create PostgreSQL data directory and log directory with proper permissions
RUN mkdir -p /var/lib/postgresql/data /app/logs && \
    chown -R postgres:postgres /var/lib/postgresql/data /app/logs

# Create startup script with proper log file location
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'set -e' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Initialize PostgreSQL if not already done' >> /app/start.sh && \
    echo 'if [ ! -f /var/lib/postgresql/data/PG_VERSION ]; then' >> /app/start.sh && \
    echo '    echo "Initializing PostgreSQL database..."' >> /app/start.sh && \
    echo '    su - postgres -c "/usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/data"' >> /app/start.sh && \
    echo '    echo "Starting PostgreSQL temporarily..."' >> /app/start.sh && \
    echo '    su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data -l /app/logs/postgresql.log start"' >> /app/start.sh && \
    echo '    sleep 5' >> /app/start.sh && \
    echo '    echo "Creating database and user..."' >> /app/start.sh && \
    echo '    su - postgres -c "createdb utm_db"' >> /app/start.sh && \
    echo '    su - postgres -c "psql -c \"CREATE USER utm_user WITH PASSWORD '\''secure_password'\''\""' >> /app/start.sh && \
    echo '    su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE utm_db TO utm_user\""' >> /app/start.sh && \
    echo '    su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data stop"' >> /app/start.sh && \
    echo 'fi' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Start PostgreSQL' >> /app/start.sh && \
    echo 'echo "Starting PostgreSQL..."' >> /app/start.sh && \
    echo 'su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data -l /app/logs/postgresql.log start"' >> /app/start.sh && \
    echo 'sleep 5' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Run migrations' >> /app/start.sh && \
    echo 'echo "Running database migrations..."' >> /app/start.sh && \
    echo 'cd /app' >> /app/start.sh && \
    echo 'export DATABASE_URL="postgresql://utm_user:secure_password@localhost:5432/utm_db"' >> /app/start.sh && \
    echo 'alembic upgrade head' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Start FastAPI application' >> /app/start.sh && \
    echo 'echo "Starting FastAPI application..."' >> /app/start.sh && \
    echo 'exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose port
EXPOSE $PORT

# Use the startup script
CMD ["/app/start.sh"]
