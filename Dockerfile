# For documentation for this Dockerfile, see: ./docs/dockerfile.md

# ------------------------------------------------------------------------------
# Builder Stage
# ------------------------------------------------------------------------------
ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION}-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

# Install dependencies from lockfile
RUN poetry build -f wheel

# ------------------------------------------------------------------------------
# Production Stage
# ------------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
# Application Environment Variables
ENV DEFAULT_RUNS=10000000

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --from=builder /app/dist/*.whl ./
RUN pip install *.whl && rm *.whl

# Switch to non-root user
USER appuser

EXPOSE 5100
CMD ["uvicorn", "montecarlo_pi.api.main:app", "--host", "0.0.0.0", "--port", "5100"]
