import logging
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from .config import settings

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRY = 1


# 对用户密码hash加密
def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


# 用户登录时输入密码和数据库hash密码比对
def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


# 创建访问令牌，用户数据、过期时间、是否刷新
def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    if expiry is None:
        expiry = timedelta(hours=ACCESS_TOKEN_EXPIRY)

    payload = {
        "user": user_data,
        "exp": datetime.now(timezone.utc) + expiry,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }
    # 编码token，包含payload定义的所有信息
    return jwt.encode(
        payload=payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHMA
    )


# 解码token，使其可以获取payload信息
def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHMA
        )
        return token_data
    except jwt.ExpiredSignatureError:
        logging.warning("token 已经过期")
        return None
    except jwt.InvalidTokenError as e:
        logging.warning(f"错误的token：{e}")
        return None
