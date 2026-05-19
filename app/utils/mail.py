from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

# 发送邮件配置
config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)

# 创建邮件发送引擎
mail = FastMail(config=config)


# 构造邮件
def create_message(recipient: list[str], subject: str, body: str):

    message = MessageSchema(
        recipients=recipient, subject=subject, body=body, subtype=MessageType.html
    )
    return message
