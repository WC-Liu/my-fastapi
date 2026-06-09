import uuid
from unittest.mock import AsyncMock, MagicMock
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.dependencies import get_current_user, get_current_active_superuser
from app.db.db import get_session
from app.main import app
from app.models.models import User


@pytest.fixture
def mock_db_session():
    """mock 数据库会话，替换 get_session 依赖"""
    session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.first.return_value = None
    mock_result.all.return_value = []
    session.exec.return_value = mock_result

    return session


@pytest_asyncio.fixture
def mock_user():
    """标准 mock 用户"""
    return User(
        uid=uuid.uuid4(),
        username="testuser",
        email="test@example.com",
        password_hashed="$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5y0x1y1y1y1y1y1y1y1y1O",
        is_active=True,
        is_superuser=False,
    )


@pytest_asyncio.fixture
async def async_client(mock_db_session):
    """异步 HTTP 客户端，注入 mock 数据库会话"""

    async def override_get_session():
        yield mock_db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def authed_client(mock_db_session, mock_user):
    """已登录用户的异步 HTTP 客户端"""

    async def override_get_session():
        yield mock_db_session

    async def override_get_current_user():
        yield mock_user

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_get_current_user
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def superuser_client(mock_db_session, mock_user):
    """超级管理员的异步 HTTP 客户端"""
    superuser = User(
        uid=uuid.uuid4(),
        username="admin",
        email="admin@example.com",
        password_hashed="dummyhash",
        is_active=True,
        is_superuser=True,
    )

    async def override_get_session():
        yield mock_db_session

    async def override_get_current_active_superuser():
        yield superuser

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_active_superuser] = (
        override_get_current_active_superuser
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        yield client
    app.dependency_overrides.clear()
