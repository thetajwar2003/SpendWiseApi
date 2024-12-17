from app import create_app
import pytest
from dotenv import load_dotenv
import os

# Load environment variables for testing
load_dotenv(dotenv_path=".env.testing")

# Import create_app correctly using absolute import


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
