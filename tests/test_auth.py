from unittest.mock import AsyncMock, patch
import pytest_asyncio
import pytest
from app.core.security import generate_passwd_hash, create_url_safe_token
from app.models.models import User
from app.utils import exceptions

pytestmark = pytest.mark.asyncio

auth_prefix = "/api/v1/auth"

REGISTER_DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
}


class TestRegister:
    async def test_register_success(self, async_client):
        """注册成功：返回 201 和用户信息"""
        with (
            patch(
                "app.service.auth_service.user_service.get_user_by_email",
                side_effect=exceptions.UserNotFoundError,
            ),
            patch(
                "app.routers.auth.mail_service.send_verify_email",
                new=AsyncMock(),
            ),
        ):
            resp = await async_client.post(
                f"{auth_prefix}/register", json=REGISTER_DATA
            )
        assert resp.status_code == 201
        body = resp.json()
        assert body["code"] == 201
        assert body["data"]["username"] == "testuser"
        assert body["data"]["email"] == "test@example.com"

    async def test_register_duplicate_email(self, async_client):
        """注册重复邮箱：返回 400"""
        with patch(
            "app.routers.auth.auth_service.create_user",
            side_effect=exceptions.UserAlreadyExistsError,
        ):
            resp = await async_client.post(
                f"{auth_prefix}/register", json=REGISTER_DATA
            )
        assert resp.status_code == 400
        # assert "已注册" in resp.text or "已存在" in resp.text

    async def test_register_invalid_data(self, async_client):
        """注册数据不合法：密码太短"""
        resp = await async_client.post(
            f"{auth_prefix}/register",
            json={"username": "u", "email": "u@u.com", "password": "12"},
        )
        assert resp.status_code == 422


class TestLogin:
    async def test_login_success(self, async_client):
        """登录成功：返回 access_token 和 refresh_token"""
        mock_user = User(
            username="testuser",
            email="test@example.com",
            password_hashed=generate_passwd_hash("testpass123"),
            is_active=True,
        )
        with patch(
            "app.service.auth_service.user_service.get_user_by_email",
            return_value=mock_user,
        ):
            resp = await async_client.post(
                f"{auth_prefix}/login",
                data={"username": "test@example.com", "password": "testpass123"},
            )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"

    async def test_login_wrong_password(self, async_client):
        """登录密码错误：返回 400"""
        mock_user = User(
            username="testuser",
            email="test@example.com",
            password_hashed=generate_passwd_hash("correctpass"),
            is_active=True,
        )

        with patch(
            "app.service.auth_service.user_service.get_user_by_email",
            return_value=mock_user,
        ):
            resp = await async_client.post(
                f"{auth_prefix}/login",
                data={"username": "test@example.com", "password": "wrongpass"},
            )

        assert resp.status_code == 400


class TestMe:
    async def test_me_authenticated(self, authed_client):
        """已登录用户获取个人信息：成功"""
        resp = await authed_client.get(f"{auth_prefix}/me")

        assert resp.status_code == 200
        body = resp.json()
        assert body["code"] == 200
        assert body["data"]["email"] == "test@example.com"
        assert body["data"]["username"] == "testuser"

    async def test_me_unauthenticated(self, async_client):
        """未登录用户获取个人信息：返回 401"""
        resp = await async_client.get(f"{auth_prefix}/me")

        assert resp.status_code == 401


class TestRefreshToken:
    async def test_refresh_without_token(self, async_client):
        """刷新令牌时未登录：返回 401"""
        resp = await async_client.post(
            f"{auth_prefix}/refresh",
            json={"refresh_token": "some_token"},
        )

        assert resp.status_code == 401


class TestVerifyEmail:
    async def test_verify_email_success(self, async_client):
        with patch(
            "app.routers.auth.mail_service.actived_user",
            new=AsyncMock(),
        ):
            resp = await async_client.get(f"{auth_prefix}/verify/some-email-token")

        assert resp.status_code == 200
        body = resp.json()
        assert body["message"] == "账号创建成功"


class TestLogout:
    async def test_logout_success(self, authed_client):
        with (
            patch("app.routers.auth.auth_service.logout_user", new=AsyncMock()),
        ):
            resp = await authed_client.get(
                f"{auth_prefix}/logout",
                headers={"Authorization": "Bearer dummy-token"},
            )
        print(resp.json())
        assert resp.status_code == 200
        body = resp.json()
        assert body["message"] == "已成功注销"

    async def test_logout_unauthenticated(self, async_client):
        resp = await async_client.get(f"{auth_prefix}/logout")
        assert resp.status_code == 401


class TestPasswordReset:
    async def test_password_reset_request_success(self, async_client):
        with patch("app.routers.auth.mail_service.password_reset", new=AsyncMock()):
            resp = await async_client.post(
                f"{auth_prefix}/password-reset-request",
                json={"email": "test@example.com"},
            )
        assert resp.status_code == 200
        body = resp.json()
        assert body["message"] == "请检查你的邮箱并重置你的密码"

    async def test_password_reset_confirm_success(self, async_client):
        with patch(
            "app.routers.auth.mail_service.reset_password",
            new=AsyncMock(),
        ):
            resp = await async_client.post(
                f"{auth_prefix}/password-reset-confirm/some-token",
                json={"new_password": "newpass123", "confirm": "newpass123"},
            )
        assert resp.status_code == 200
        body = resp.json()
        assert body["message"] == "密码修改成功"
