from uuid import uuid4

from passlib.hash import bcrypt
from sqlalchemy import select

from app.models import User


class AuthError(Exception):
    pass


class PermissionDenied(Exception):
    pass


class NotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


class ConflictError(Exception):
    pass


class BadRequestError(Exception):
    pass


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.verify(password, password_hash)


def generate_token() -> str:
    return uuid4().hex


async def get_current_user(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthError("Требуется заголовок Authorization: Bearer <token>")

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        raise AuthError("Пустой токен")

    async with request.app["db_sessionmaker"]() as session:
        result = await session.execute(select(User).where(User.token == token))
        user = result.scalar_one_or_none()

    if user is None:
        raise AuthError("Неверный токен")

    return user
