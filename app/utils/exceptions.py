# 用户模块
class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UserDisabledError(Exception):
    pass


# 认证模块
class UnauthorizedError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class AccessTokenRequired(Exception):
    pass


class RefreshTokenRequired(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


# 电影模块
class MovieNotFoundError(Exception):
    pass


class MovieAlreadyExistsError(Exception):
    pass
