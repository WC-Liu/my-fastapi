import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from itsdangerous import URLSafeTimedSerializer
from pwdlib import PasswordHash

from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

passwd_context = PasswordHash.recommended()
ACCESS_TOKEN_EXPIRY = 1
REFRESH_TOKEN_EXPIRY = 2
DUMMY_HASH = passwd_context.hash("dummypassword")


# -------------------1. 用户密码hash功能块------------------
def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


# -------------------2. JWT功能块------------------
def create_access_token(
    subject: str | Any, expiry: timedelta = None, refresh: bool = False
):
    if expiry is None:
        expiry = timedelta(hours=ACCESS_TOKEN_EXPIRY)

    payload = {
        "sub": str(subject),
        "exp": datetime.now(timezone.utc) + expiry,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }
    return jwt.encode(
        payload=payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM
        )
        return token_data
    except jwt.ExpiredSignatureError:
        logger.warning("token 已经过期")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"错误的token：{e}")
        return None


# -------------------3. 邮箱验证功能块------------------
serializer = URLSafeTimedSerializer(
    secret_key=settings.JWT_SECRET, salt="email-configuration"
)


def create_url_safe_token(data: dict):
    token = serializer.dumps(data)
    return token


def decode_url_safe_token(token: str) -> dict:
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logger.error(str(e))
