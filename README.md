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
