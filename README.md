# Tansy

Tansy is a containerized Python application that determines &pi; via Monte Carlo simulation.

## Setup

```zsh
# Clone
git clone https://github.com/herereadthis/tansy
cd tansy
# Install Poetry if you haven't already
brew install poetry
# Create Virtual env and install dependencies
poetry install
```

## Testing

```zsh
# run pytest
poetry run nox -s tests
# run pylint
poetry run nox -s lint
# run both
poetry run nox -s check
```

## Usage

```zsh
# Run the simulation
poetry run montecarlo-pi
```

### Container

You can run this application locally as a docker container.

```zsh
# Build
docker build -t montecarlo-pi .

# Run the container
docker run --rm -p 5100:5100 montecarlo-pi

# Health check
curl localhost:5100/health
```


___

## Deprecated notes

### Container

Previously, this project was a CLI tool. The `Dockerfile` had:

```sh
ENTRYPOINT ["montecarlo-pi"]
CMD []
```

To run the CLI:

```zsh
# Build
docker build -t montecarlo-pi .

# Run with default
docker run --rm montecarlo-pi

# Run with arguments
docker run --rm montecarlo-pi [your-cli-arguments]
```