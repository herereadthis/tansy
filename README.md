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
# Test on local env on port 5101
poetry run nox -s dev
# Confirm it works
curl http://localhost:5101/health

# Alternative: run the simulation as a cli
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
# simulate pi
curl http://localhost:5101/simulate/pi
# simulate pi, specify simulations
curl http://localhost:5101/simulate/pi?sample_size=100000&pretty=true
```

### Application structure


```
tansy/                              # Root directory
├── .gitignore                      # Things to exclude from version control
├── Dockerfile                      # Docker Container specification
├── README.md                       # Main documentation
├── noxfile.py                      # Task automation config via Nox
├── poetry.lock                     # Poetry dependency lock file 
├── pyproject.toml                  # Project config, metadata, dependencies
│
├── scripts/                        # Utility scripts
│   └── test_and_lint.py            # QA automation
│
├── src/                            # Application source code
│   └── montecarlo_pi/              # Main package
│       ├── __init__.py             # Package marker
│       ├── cli.py                  # Terminal Interface (CLI entry point)
│       ├── exceptions.py           # Custom exception classes
│       │
│       ├── api/                    # HTTP interface layer (FastAPI REST API)
│       │   ├── __init__.py         Package marker
│       │   ├── main.py             # Interface Module (FastAPI app instance)
│       │   └── routers/            # API route modules
│       │       ├── __init__.py     # Package marker
│       │       └── health.py       # Service status router
│       │       └── simulation.py   # Simulation endpoint router
│       │
│       ├── simulation/             # Business logic
│       │   ├── __init__.py         # Package marker
│       │   ├── service.py          # Orchestration layer
│       │   ├── chudnovsky.py       # Business logic module (validation)
│       │   └── pi_simulation.py    # Business logic module (core computation)
│       │
│       └── utilities/              # Shared helpers
│           ├── __init__.py         # Package marker
│           ├── constants.py        # Constants
│           └── util.py             # Common utilities module
│
└── tests/                          # Test suite
    ├── test_boilerplate.py         # Setup validation tests
    ├── test_api.py                 # Test module for endpoints
    ├── test_pi_simulation.py       # Test module for business logic
    └── test_util.py                # Test module for utilities
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




```
Future work, signal handling

import signal
import sys

def signal_handler(signum, frame):
    print("Received signal, shutting down gracefully...")
    sys.exit(0)

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)  # K8s sends SIGTERM
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
```
