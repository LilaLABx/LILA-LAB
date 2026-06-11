# ─────────────────────────────────────────────────────────
# {PIPELINE_NAME} — Makefile
# Pipeline-specific tasks for development and maintenance.
# ─────────────────────────────────────────────────────────

SHELL := /bin/bash
PYTHON := python3

.PHONY: install lint format test clean help

# ── Install ────────────────────────────────────────────

install:
	$(PYTHON) -m pip install -r requirements.txt

# ── Lint & Format ─────────────────────────────────────

lint:
	ruff check . --ignore E501

format:
	ruff format . --check

format-fix:
	ruff format .

# ── Tests ──────────────────────────────────────────────

test:
	$(PYTHON) -m pytest -v --tb=short

# ── Cleanup ───────────────────────────────────────────

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# ── Help ──────────────────────────────────────────────

help:
	@echo "{PIPELINE_NAME} — Makefile"
	@echo ""
	@echo "install       Install pipeline dependencies"
	@echo "lint          Lint code with Ruff"
	@echo "format        Check formatting (dry-run)"
	@echo "format-fix    Apply formatting fixes"
	@echo "test          Run pytest"
	@echo "clean         Remove build artifacts"
	@echo ""
	@echo "See repo root Makefile for lab-wide tasks."
