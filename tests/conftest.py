from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker
from app.db.db import get_session
from app.main import app

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(["admin"])

mock_session = Mock()
mock_user_service = Mock()
mock_movie_service = Mock()


def get_mock_session():
    yield mock_session


app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer] = Mock()


@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_user_service():
    return mock_user_service


@pytest.fixture
def fake_movie_service():
    return mock_movie_service


@pytest.fixture
def test_client():
    return TestClient(app)
