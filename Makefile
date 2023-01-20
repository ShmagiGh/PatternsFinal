.PHONY: help
.DEFAULT_GOAL := help

help:
	echo "There was, not help, no help from you!"

install: ## Install requirements
	pip install -r requirements.txt

format: ## Run code formatters
	isort app test
	black app test

lint: ## Run code linters
	isort --check app test
	black --check app test
	flake8 app test
	mypy app test

test:  ## Run tests with coverage
	pytest --cov
