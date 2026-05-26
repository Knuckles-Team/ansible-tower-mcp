# tests/conftest.py
import pytest
from unittest.mock import MagicMock

# CONCEPT:ANSIBLE-05: Standardized Test Fixtures and Mocks


@pytest.fixture
def mock_api():
    """Fixture to provide a mocked Ansible Tower API client."""
    mock = MagicMock()
    return mock
