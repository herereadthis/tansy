# Dockerfile 

## Builder Stage

* This dockerfile uses multi-stage builds. Tutorial at [testdriven.io](ttps://testdriven.io/blog/docker-best-practices/#use-multi-stage-builds)
* Python environment variables, docs at docs.python.orghttps://docs.python.org/3/using/cmdline.html#environment-variables
  ```Dockerfile
  # Do not generate .pyc files
  ENV PYTHONDONTWRITEBYTECODE=1
  # Force stdout and stderr to be unbuffered for Docker logs
  ENV PYTHONUNBUFFERED=1
  # Do not let pip cache downloads
  ENV PIP_NO_CACHE_DIR=1
  # Skip version checks to speed up installs
  ENV PIP_DISABLE_PIP_VERSION_CHECK=1
  ```
* Install System dependencies
  ```Dockerfile
  RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
  ```
  * See https://docs.docker.com/build/building/best-practices/
  * `--no-install-recommends` skip recommended installs
  * `build-essential` installs various tools you need to compile Python C extensions (including `numpy`)
  * `&& rm -rf /var/lib/apt/lists/*` Delete apt cache to reduce image size


## Production stage

* `EXPOSE 5100` Expose API port. 5100 was an arbitrarily chosen port to avoid conflicts with other commonly-used ports.
* `CMD ["uvicorn", "montecarlo_pi.api.main:app", "--host", "0.0.0.0", "--port", "5100"]`
  * This line runs the FastAPI server
  * To run the container, do
    ```zsh
    docker run --rm -p 5100:5100 montecarlo-pi
    ```