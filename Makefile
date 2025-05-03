.PHONY: test coverage report clean help all dev

PYTHON := python3

SRC_DIR := src
TEST_DIR := tests

test:
	$(PYTHON) -m unittest discover -s $(TEST_DIR)

coverage:
	coverage run -m unittest discover -s $(TEST_DIR)

report: coverage
	coverage report -m
	coverage html

all: test coverage report

# Development helpers
dev-setup:
	$(PYTHON) -m pip install coverage

clean:
	rm -rf htmlcov/
	rm -f .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Python Test Automation"
	@echo "======================"
	@echo
	@echo "Available commands:"
	@echo "  make test       - Run tests without coverage"
	@echo "  make coverage   - Run tests with coverage tracking"
	@echo "  make report     - Generate coverage reports (requires running coverage first)"
	@echo "  make all        - Run tests and generate coverage reports"
	@echo "  make dev-setup  - Install development dependencies"
	@echo "  make clean      - Remove coverage data and cache files"
	@echo
	@echo "Example usage:"
	@echo "  make all        - Complete test suite with coverage"