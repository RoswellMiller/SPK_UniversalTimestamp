# Makefile for SPK Universal Timestamp development

.PHONY: help install install-dev test test-cov lint format type-check clean build upload-test upload docs

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=SPK_UniversalTimestamp --cov-report=html --cov-report=term

lint:  ## Run linting
	flake8 SPK_UniversalTimestamp Tests

format:  ## Format code with black and isort
	black .
	isort .

type-check:  ## Run type checking
	mypy SPK_UniversalTimestamp

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build the package
	python -m build

check-build:  ## Check the built package
	twine check dist/*

upload-test:  ## Upload to TestPyPI
	twine upload --repository testpypi dist/*

upload:  ## Upload to PyPI
	twine upload dist/*

docs:  ## Generate documentation (if using Sphinx)
	@echo "Documentation generation not yet configured"

all: format lint type-check test  ## Run all quality checks
