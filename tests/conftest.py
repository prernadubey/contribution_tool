from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from components.controller.fastapi.main import create_component


@pytest.fixture
def fastapi_test_client():
    app = create_component(middleware_enabled=False)
    return TestClient(app)


@pytest.fixture
def db_session_mock():
    return AsyncMock()
