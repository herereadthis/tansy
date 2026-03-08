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

* This project uses `nox` to do repetitive tasks that would otherwise be easy to forget.
* See `/noxfile.py` for all tasks 

```zsh
# run pytest
poetry run nox -s tests
# run pylint
poetry run nox -s lint
# run both
poetry run nox -s check
```

## Local testing and development

* Note that for local development, the FastAPI server runs on port `5101`.
* This port is different than the `5100` port for the Docker image, in order avoid collisions.

```zsh
# Test on local env on port 5101
poetry run nox -s dev
# Confirm it works
curl http://localhost:5101/health

# Alternative: run the simulation as a cli
poetry run montecarlo-pi
```

## Container

You can run this application locally as a docker container.

```zsh
# Build
# When testing, you don't want to build from a working cache, so use --no-cache
docker build --no-cache -t montecarlo-pi .
# Run the container
docker run --rm -p 5100:5100 montecarlo-pi
# Health check
curl localhost:5100/health
# simulate pi
curl http://localhost:5100/simulate/pi
# simulate pi, specify simulations
curl http://localhost:5100/simulate/pi?sample_size=100000&pretty=true
```

#### Pulling the image

```zsh
docker pull ghcr.io/herereadthis/tansy:latest
docker run --rm -p 5100:5100 ghcr.io/herereadthis/tansy:latest
curl localhost:5100/health
```

## Future planned work

This project is an "embarrassingly parallel" workdload



## Application structure


```
tansy/                              # Root directory
├── .gitignore                      # Things to exclude from version control
├── Dockerfile                      # Docker Container specification
├── README.md                       # Main documentation
├── noxfile.py                      # Task automation config via Nox
├── poetry.lock                     # Poetry dependency lock file 
├── pyproject.toml                  # Project config, metadata, dependencies
├── .github/                        # GitHub Actions workflows
│   └── workflows/
│       └── build.yml               # CI/CD pipeline
├── .vscode/                        # VS Code workspace settings
│   ├── extensions.json             # Recommended extensions
│   └── settings.json               # Workspace settings
├── docs/                           # Documentation
│   └── dockerfile.md               # Dockerfile documentation
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
│       │   ├── __init__.py         # Package marker
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

## Layered Architecture

This application aims to use well-documented patterns of software architecture. When you make a request, the app goes to the router, then service, and then the computation, which is what runs the Monte Carlo simulation. The reasoning is separation of concerns:

1. The router layer (`simulation.py`) does not contain business logic. By containing the router, we can remove FastAPI and replace with something else (or even use a CLI), without having to change the orchestration code.
2. The service layer (`service.py`) does not have any computation, so we can swap out the current simulation with some other simulation (there are multiple ways to simulate &pi;), without having to alter the business logic.
3. The computation layer (`pi_simulation.py`) is isolated from business logic, so it will be easy to write unit tests. Compared to popular texts on layered architecture, the computation layer replaces the Data Access layer because there's no persistent state.


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
