import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

class MockLimiter:
    def __init__(self):
        self.exempt = set()
        self.enabled = True
        self.failure_headers = {}
        self._exempt_routes = set()
        self._route_limits = {}
        self._auto_check = False  # <-- Adicione esta linha

    def limit(self, limit_value):
        def decorator(func):
            func.__name__ = getattr(func, '__name__', 'unknown')
            func.__module__ = getattr(func, '__module__', 'unknown')
            return func
        return decorator

    async def check(self):
        return True

    def reset(self):
        pass

mock_redis = MagicMock()
mock_limiter = MockLimiter()

with patch('redis.asyncio.Redis', return_value=mock_redis), \
     patch('slowapi.Limiter', return_value=mock_limiter):
    from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_auth_headers():
    return {"Authorization": "Bearer test"}

@pytest.fixture
def invalid_auth_headers():
    return {"Authorization": "Bearer invalid-token"}