.PHONY: help install generate test lint format clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv pip install -e ".[dev]"

generate:  ## Generate Pydantic models from OpenAPI spec
	@./scripts/generate_models.sh

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=src/novita --cov-report=html --cov-report=term

lint:  ## Run linting
	ruff check src/ tests/ examples/

lint-fix:  ## Run linting with auto-fix
	ruff check --fix src/ tests/ examples/

format:  ## Format code
	ruff format src/ tests/ examples/

typecheck:  ## Run type checking
	mypy src/

ci:  ## Run all CI checks (lint, format check, typecheck, test)
	ruff check src/ tests/ examples/
	ruff format --check src/ tests/ examples/
	mypy src/
	pytest tests/ -v

clean:  ## Clean generated files and caches
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-generated:  ## Clean generated models
	rm -f src/novita/generated/models.py

spec-validate:  ## Validate OpenAPI spec (requires openapi-spec-validator)
	@if command -v openapi-spec-validator >/dev/null 2>&1; then \
		openapi-spec-validator openapi/novita-api.yaml; \
	else \
		echo "Install openapi-spec-validator: pip install openapi-spec-validator"; \
	fi

.DEFAULT_GOAL := help