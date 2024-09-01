#!/bin/bash


# Run black
echo "Running black..."
black . --check --config=./pyproject.toml

# Run isort
echo "Running isort..."
isort . --check-only --profile=black

# Running ruff
echo "Running ruff..."
ruff check --config=./pyproject.toml .

# Running bandit
echo "Running bandit..."
bandit -c pyproject.toml -r .

# Run linter
echo "Running linter..."
pylint *.py --rcfile=./pyproject.toml
