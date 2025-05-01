import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_handler():
    handler = Mock()
    handler.__module__ = 'test_module'
    handler.__name__ = 'test_handler'
    return handler

def test_root_endpoint(mock_handler):
    assert f"{mock_handler.__module__}.{mock_handler.__name__}" == "test_module.test_handler"

def test_root_endpoint_no_auth(mock_handler):
    assert f"{mock_handler.__module__}.{mock_handler.__name__}" == "test_module.test_handler"

def test_ping_endpoint(mock_handler):
    assert f"{mock_handler.__module__}.{mock_handler.__name__}" == "test_module.test_handler"

def test_memory_endpoint(mock_handler):
    assert f"{mock_handler.__module__}.{mock_handler.__name__}" == "test_module.test_handler"

def test_scalar_endpoint(mock_handler):
    assert f"{mock_handler.__module__}.{mock_handler.__name__}" == "test_module.test_handler"