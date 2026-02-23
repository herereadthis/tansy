# Official Python runtime is base image
# builder is for multi-stage build to install dependencies
ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION}-slim AS builder
ARG PYTHON_VERSION

# environment Variables ========================================================
# Reference: https://docs.python.org/3/using/cmdline.html#environment-variables
# Do not generate .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Force stdout and stderr to be unbuffered for Docker logs
ENV PYTHONUNBUFFERED=1
# Do not let pip cache downloads
ENV PIP_NO_CACHE_DIR=1
# Skip version checks to speed up installs
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
# See https://docs.docker.com/build/building/best-practices/
RUN apt-get update && apt-get install -y --no-install-recommends \
    # required to compile Python packages with C extensions
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

# Install dependencies from lockfile
RUN poetry config virtualenvs.create false && poetry install --only main


# Production stage. For multi-stage builds, see:
# https://testdriven.io/blog/docker-best-practices/#use-multi-stage-builds
FROM python:${PYTHON_VERSION}-slim AS production
ARG PYTHON_VERSION

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application Environment Variables
ENV DEFAULT_RUNS=10000000

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Switch to non-root user
USER appuser

# Install the application in user mode
# RUN pip install --user --no-deps .

# Add user's local bin to PATH
ENV PATH="/home/appuser/.local/bin:$PATH"

# Set default command
# This was appropriate when the application was installed as a CLI tool
# In that case, the correct command to run would have been:
# docker run --rm montecarlo-pi
# ENTRYPOINT ["montecarlo-pi"]
# CMD []

# Expose API port
EXPOSE 5100

# Run FastAPI server
# To run the container:
# docker run --rm -p 5100:5100 montecarlo-pi
CMD ["uvicorn", "montecarlo_pi.api.main:app", "--host", "0.0.0.0", "--port", "5100"]