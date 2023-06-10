FROM python:3.11

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy pyproject.toml and install Python dependencies
COPY pyproject.toml /app/
RUN pip install poetry --cache-dir /tmp/pip-cache && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Copy app code
COPY . /app/

# Run migrations
RUN poetry run alembic upgrade head
