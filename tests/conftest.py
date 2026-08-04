import sys
import os
import pytest

# Ensure app directory is in Python path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/flask-api')))

from app import app as flask_app

@pytest.fixture
def app():
    """Yield application instance for testing."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()
