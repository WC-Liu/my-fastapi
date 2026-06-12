from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import (
    create_url_safe_token,
    decode_url_safe_token,
    generate_passwd_hash,
)
from app.schemas.auth import PasswordResetConfirm
from app.utils import exceptions
from app.utils.celery import send_email

from .user_service import user_service


class MailService:
    async def send_verify_email(self, email: str) -> None:
        token = create_url_safe_token({"email": email})

        link = f"http://localhost:8000/api/v1/auth/verify/{token}"
        html_message = f"""
        <h1>验证邮箱</h1>
        <p>请点击这个链接 <a href="{link}">link</a> 验证你的邮箱<p>
        """
        emails = [email]
        subject = "验证你的邮箱"
        send_email.delay(emails, subject, html_message)

    async def activated_user(
        self, email_token: str, user_data: dict, session: AsyncSession
    ) -> None:
        token_data = decode_url_safe_token(email_token)
        user_email = token_data.get("email")
        if user_email:
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise exceptions.UserNotFoundError()
            for k, v in user_data.items():
                setattr(user, k, v)
            await session.commit()

    async def password_reset(self, email: str, session: AsyncSession) -> None:
        user = await user_service.get_user_by_email(email, session)
        if user:
            token = create_url_safe_token({"email": email, "sub": str(user.uid)})

            link = f"http://localhost:8000/api/v1/auth/password-reset-confirm/{token}"
            html_message = f"""
            <h1>重置密码</h1>
            <p>请点击这个链接 <a href="{link}">link</a> 重置你的密码<p>
            """
            emails = [email]
            subject = "重置你的密码"
            send_email.delay(emails, subject, html_message)

    async def reset_password(
        self,
        email_token: str,
        passwords: PasswordResetConfirm,
        session: AsyncSession,
    ) -> None:
        if passwords.new_password != passwords.confirm:
            raise exceptions.PasswordNotMatch()
        token_data = decode_url_safe_token(email_token)
        if not token_data:
            raise exceptions.InvalidTokenError()
        user_uid = token_data.get("sub")
        if not user_uid:
            raise exceptions.InvalidTokenError()
        user = await user_service.get_user_by_user_uid(user_uid, session)
        if not user:
            raise exceptions.UserNotFoundError()
        new_password_hash = generate_passwd_hash(passwords.new_password)
        user.password_hashed = new_password_hash
        await session.commit()


mail_service = MailService()
