from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import (
    create_url_safe_token,
    decode_url_safe_token,
)
from app.utils import exceptions
from app.utils.mail import create_message, mail

from .user_service import user_service


class MailService:
    async def send_verify_email(self, email: str, session: AsyncSession):
        token = create_url_safe_token({"email": email})

        link = f"http://localhost:8000/api/v1/auth/verify/{token}"
        html_message = f"""
        <h1>验证邮箱</h1>
        <p>请点击这个链接 <a href="{link}">link</a> 验证你的邮箱<p>
        """
        message = create_message(recipient=[email], subject="欢迎", body=html_message)
        try:
            await mail.send_message(message)
        except Exception:
            raise exceptions.MailServiceError()

    async def verified_user(
        self, email_token: str, user_data: dict, session: AsyncSession
    ):
        token_data = decode_url_safe_token(email_token)
        user_email = token_data.get("email")
        if user_email:
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise exceptions.UserNotFoundError()
            for k, v in user_data.items():
                setattr(user, k, v)
            await session.commit()
        return JSONResponse(content={"messages": "账号创建成功"}, status_code=200)


mail_service = MailService()
