FROM python:3.11-bullseye

WORKDIR /app

# Install system deps
RUN apt-get update \
 && apt-get install -y \
     build-essential \
     curl \
     gcc \
     git \
     libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project files
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi
COPY . /app

# Default environment
ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
