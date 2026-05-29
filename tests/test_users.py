import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest

from app.models.models import User
from app.utils import exceptions

pytestmark = pytest.mark.asyncio

users_prefix = "/api/v1/users"


def _make_user(**overrides) -> User:
    """辅助函数：创建真实 User 实例"""
    data = {
        "uid": uuid.uuid4(),
        "username": "testuser",
        "email": "test@example.com",
        "password_hashed": "dummyhash",
        "is_active": True,
        "is_superuser": False,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    data.update(overrides)
    return User(**data)


class TestGetUsers:
    async def test_get_users_as_superuser(self, superuser_client):
        users = [
            _make_user(username="alice", email="alice@example.com"),
            _make_user(
                username="admin",
                email="admin@example.com",
                is_superuser=True,
            ),
        ]

        with patch(
            "app.routers.users.user_service.get_all_users",
            new=AsyncMock(return_value=users),
        ):
            resp = await superuser_client.get(f"{users_prefix}/")

        assert resp.status_code == 200
        body = resp.json()
        assert len(body) == 2
        assert body[0]["username"] == "alice"
        assert body[1]["username"] == "admin"

    async def test_get_users_as_normal_user(self, authed_client):
        resp = await authed_client.get(f"{users_prefix}/")
        assert resp.status_code == 403


class TestGetUser:
    async def test_get_user_by_uid_as_superuser(self, superuser_client):
        user = _make_user(username="alice", email="alice@example.com")

        with patch(
            "app.routers.users.user_service.get_user_by_user_uid",
            new=AsyncMock(return_value=user),
        ):
            resp = await superuser_client.get(f"{users_prefix}/{user.uid}")

        assert resp.status_code == 200
        body = resp.json()
        assert body["username"] == "alice"
        assert body["email"] == "alice@example.com"

    async def test_get_user_not_found(self, superuser_client):
        with patch(
            "app.routers.users.user_service.get_user_by_user_uid",
            side_effect=exceptions.UserNotFoundError,
        ):
            resp = await superuser_client.get(
                f"{users_prefix}/{uuid.uuid4()}"
            )

        assert resp.status_code == 404


class TestUpdateUser:
    async def test_update_user_as_superuser(self, superuser_client):
        user = _make_user(username="updated_name")

        with patch(
            "app.routers.users.user_service.update_user",
            new=AsyncMock(return_value=user),
        ):
            resp = await superuser_client.patch(
                f"{users_prefix}/{user.uid}",
                json={"username": "updated_name"},
            )
        assert resp.status_code == 200
        assert resp.json()["username"] == "updated_name"

    async def test_update_user_as_normal_user(self, authed_client):
        resp = await authed_client.patch(
            f"{users_prefix}/{uuid.uuid4()}",
            json={"username": "hacker"},
        )
        assert resp.status_code == 403


class TestDeleteUser:
    async def test_delete_user_as_superuser(self, superuser_client):
        with patch(
            "app.routers.users.user_service.delete_user",
            new=AsyncMock(),
        ):
            resp = await superuser_client.delete(
                f"{users_prefix}/{uuid.uuid4()}"
            )

        assert resp.status_code == 204

    async def test_delete_user_as_normal_user(self, authed_client):
        resp = await authed_client.delete(
            f"{users_prefix}/{uuid.uuid4()}"
        )
        assert resp.status_code == 403

    async def test_delete_user_not_found(self, superuser_client):
        with patch(
            "app.routers.users.user_service.delete_user",
            side_effect=exceptions.UserNotFoundError,
        ):
            resp = await superuser_client.delete(
                f"{users_prefix}/{uuid.uuid4()}"
            )

        assert resp.status_code == 404