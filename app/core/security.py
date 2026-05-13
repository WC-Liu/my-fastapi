from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)
