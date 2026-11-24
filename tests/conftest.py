"""Shared test setup: page discovery and the ``page_path`` parametrization.

The repo root is put on ``sys.path`` by ``pythonpath = ["."]`` in pyproject.toml.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "pages"
APP_FILE = ROOT / "app.py"


def page_number(path):
    match = re.match(r"\d+", path.name)
    return int(match.group()) if match else -1


def page_files():
    """Every pages/*.py file, sorted by its numeric prefix (2 before 10)."""
    return sorted(PAGES_DIR.glob("*.py"), key=lambda p: (page_number(p), p.name))


def pytest_generate_tests(metafunc):
    """Any test that takes a ``page_path`` argument runs once per page, with the file stem as id."""
    if "page_path" in metafunc.fixturenames:
        pages = page_files()
        metafunc.parametrize("page_path", pages, ids=[p.stem for p in pages])


@pytest.fixture(scope="session")
def repo_root():
    return ROOT


@pytest.fixture(scope="session")
def app_file():
    return APP_FILE


@pytest.fixture(scope="session")
def all_pages():
    return page_files()
