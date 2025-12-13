.PHONY: help install generate test test-integration test-all test-cov lint lint-fix format typecheck pre-commit-test pre-commit-install pre-commit-run ci clean clean-generated spec-validate build publish-pypi publish-test

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv pip install -e ".[dev]"

generate:  ## Generate Pydantic models from OpenAPI spec
	@./scripts/generate_models.sh

test:  ## Run unit tests only
	pytest tests/unit/ -v

test-integration:  ## Run safe integration tests (requires NOVITA_API_KEY)
	@if [ -z "$$NOVITA_API_KEY" ]; then \
		echo "Error: NOVITA_API_KEY environment variable not set"; \
		echo "Run: export NOVITA_API_KEY='your-key-here'"; \
		exit 1; \
	fi
	pytest tests/integration/ -m "integration and not invasive" -v

test-all:  ## Run all tests (unit + safe integration)
	@$(MAKE) test
	@$(MAKE) test-integration

test-cov:  ## Run tests with coverage
	pytest tests/unit --cov=novita --cov-report=html --cov-report=term-missing

lint:  ## Run linting
	ruff check src/ tests/ examples/

lint-fix:  ## Run linting with auto-fix
	ruff check --fix src/ tests/ examples/

format:  ## Format code
	ruff format src/ tests/ examples/

typecheck:  ## Run type checking
	mypy src/

pre-commit-test:  ## Run unit tests (fast, for pre-commit hook)
	@pytest tests/unit/ -q --tb=line

pre-commit-install:  ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	@uv pip install pre-commit
	@pre-commit install
	@echo ""
	@echo "✅ Pre-commit hooks installed!"
	@echo ""
	@echo "Hooks will run automatically on git commit."
	@echo "To run manually: make pre-commit-run"
	@echo "To skip hooks: git commit --no-verify"

pre-commit-run:  ## Run pre-commit hooks on all files
	@pre-commit run --all-files

ci:  ## Run all CI checks (lint, format check, typecheck, test)
	@echo "Running linter..."
	@ruff check src/ tests/ examples/
	@echo ""
	@echo "Checking formatting..."
	@ruff format --check src/ tests/ examples/
	@echo ""
	@echo "Running type checker..."
	@mypy src/
	@echo ""
	@echo "Running tests..."
	@pytest tests/unit/ -v
	@echo ""
	@echo "✅ All checks passed!"

clean:  ## Clean build artifacts and caches
	rm -rf dist/ build/ *.egg-info
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-generated:  ## Clean generated models
	rm -f src/novita/generated/models.py

spec-validate:  ## Validate OpenAPI spec
	@if command -v openapi-spec-validator >/dev/null 2>&1; then \
		openapi-spec-validator openapi/novita-api.yaml; \
	else \
		echo "Install openapi-spec-validator: uv pip install openapi-spec-validator"; \
	fi

build:  ## Build distribution packages
	@$(MAKE) clean
	@uv pip install build twine
	@python -m build --sdist --wheel --outdir dist/
	@twine check dist/*
	@echo ""
	@echo "✅ Build complete! Distributions in dist/"
	@ls -lh dist/

publish-pypi: SHELL := /bin/bash
publish-pypi:  ## Publish to PyPI (interactive, requires PyPI credentials)
	@echo "🚀 Publishing to PyPI"
	@echo ""
	@echo "Pre-flight checks:"
	@echo "  1. Verify version in pyproject.toml"
	@echo "  2. Update CHANGELOG.md"
	@echo "  3. Commit all changes"
	@echo "  4. Run 'make ci' to ensure all checks pass"
	@echo ""
	@read -p "Version to publish (from pyproject.toml): " version; \
	echo ""; \
	echo "Verifying version matches..."; \
	VERSION_IN_FILE=$$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"); \
	if [ "$$VERSION_IN_FILE" != "$$version" ]; then \
		echo "❌ Error: Version in pyproject.toml ($$VERSION_IN_FILE) does not match ($$version)"; \
		exit 1; \
	fi; \
	echo "✅ Version check passed: $$version"; \
	echo ""; \
	echo "Running CI checks..."; \
	$(MAKE) ci || exit 1; \
	echo ""; \
	echo "Building distributions..."; \
	$(MAKE) build || exit 1; \
	echo ""; \
	read -p "Ready to publish v$$version to PyPI? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		echo ""; \
		echo "Publishing to PyPI..."; \
		twine upload dist/*; \
		echo ""; \
		echo "✅ Published successfully!"; \
		echo ""; \
		echo "Next steps:"; \
		echo "  1. Create git tag: git tag -a v$$version -m 'Release version $$version'"; \
		echo "  2. Push tag: git push origin v$$version"; \
		echo "  3. Create GitHub release at: https://github.com/php-workx/novita-sdk-python/releases/new"; \
	else \
		echo ""; \
		echo "❌ Publish cancelled"; \
		exit 1; \
	fi

publish-test:  ## Publish to TestPyPI for testing
	@echo "🧪 Publishing to TestPyPI"
	@$(MAKE) ci
	@$(MAKE) build
	@echo ""
	@echo "Publishing to TestPyPI..."
	@twine upload --repository testpypi dist/*
	@echo ""
	@echo "✅ Published to TestPyPI!"
	@echo ""
	@echo "Test installation with:"
	@echo "  pip install --index-url https://test.pypi.org/simple/ novita-sdk"

.DEFAULT_GOAL := help
