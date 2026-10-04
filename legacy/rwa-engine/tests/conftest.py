"""Shared fixtures: every test gets a fresh in-memory database with the seed data."""
import pytest

from rwa_app.db import get_connection, init_db

REPORTING_DATE = "2026-09-30"


@pytest.fixture
def conn():
    c = get_connection(":memory:")
    init_db(c)
    yield c
    c.close()
