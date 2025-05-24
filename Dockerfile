# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# system deps for psycopg2 / sqlalchemy
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# copy & install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# copy code
COPY . .

# run migrations (optional) then start
# if you use Alembic:
# ENTRYPOINT ["alembic", "upgrade", "head"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
