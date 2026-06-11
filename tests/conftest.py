"""
LILA Lab — Shared Test Configuration
=====================================
Pytest conftest with fixtures shared across all pipeline tests.

Run with:  pytest              (from repo root)
           pytest tests/       (explicit)
           make test           (via Makefile)
"""

from pathlib import Path

import pytest

# ── Repository root ──────────────────────────────────


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Return absolute path to the repository root."""
    return Path(__file__).resolve().parent.parent


# ── Common paths ─────────────────────────────────────


@pytest.fixture(scope="session")
def pipelines_dir(repo_root: Path) -> Path:
    return repo_root / "pipelines"


@pytest.fixture(scope="session")
def dataset_dir(repo_root: Path) -> Path:
    return repo_root / "dataset"


@pytest.fixture(scope="session")
def shared_dir(pipelines_dir: Path) -> Path:
    return pipelines_dir / "shared"


# ── Sample data helpers ──────────────────────────────


@pytest.fixture
def sample_article() -> dict:
    """Return a minimal article dict for annotation pipeline tests."""
    return {
        "id": "test-001",
        "title": "Sample article title",
        "text": "This is a sample article body for testing annotation pipelines.",
        "source": "test-source",
        "date": "2026-01-01",
        "url": "https://example.com/test-001",
    }


@pytest.fixture
def sample_articles() -> list[dict]:
    """Return a list of 5 sample articles for batch tests."""
    return [
        {
            "id": f"test-{i:03d}",
            "title": f"Article {i}",
            "text": f"This is article {i} body text for testing purposes.",
            "source": "test-source",
            "date": f"2026-01-{i:02d}",
            "url": f"https://example.com/test-{i:03d}",
        }
        for i in range(1, 6)
    ]
