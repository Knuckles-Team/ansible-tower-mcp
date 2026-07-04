# tests/conftest.py
import pytest
from unittest.mock import MagicMock

# CONCEPT:AT-OS.config.standardized-test-fixtures-mocks: Standardized Test Fixtures and Mocks


@pytest.fixture
def mock_api():
    """Fixture to provide a mocked Ansible Tower API client."""
    mock = MagicMock()
    return mock
