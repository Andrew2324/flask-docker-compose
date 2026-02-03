FROM python:3.12-slim

WORKDIR /app

# System deps for psycopg2 + curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

# Install deps first (better caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code + entrypoint
COPY app/src /app/src
COPY app/entrypoint.sh /app/entrypoint.sh

# Make entrypoint executable (do this AFTER copy)
RUN chmod +x /app/entrypoint.sh

# Ensure python can import src.*
ENV PYTHONPATH=/app

USER appuser
EXPOSE 5000

CMD ["/app/entrypoint.sh"]
