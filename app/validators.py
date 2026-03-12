from aiohttp import web

from app.auth import BadRequestError, ValidationError


async def get_json(request: web.Request) -> dict:
    try:
        data = await request.json()
    except Exception as exc:
        raise BadRequestError("Тело запроса должно быть в формате JSON") from exc

    if not isinstance(data, dict):
        raise BadRequestError("JSON должен быть объектом")
    return data


def require_fields(data: dict, fields: list[str]) -> None:
    for field in fields:
        if field not in data:
            raise ValidationError(f"Поле '{field}' обязательно")
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValidationError(f"Поле '{field}' должно быть непустой строкой")


def validate_email(value: str) -> None:
    if "@" not in value or len(value) < 5:
        raise ValidationError("Некорректный email")


def validate_password(value: str) -> None:
    if len(value) < 6:
        raise ValidationError("Пароль должен содержать не менее 6 символов")


def validate_ad_update_data(data: dict) -> None:
    allowed_fields = {"title", "description"}
    if not data:
        raise ValidationError("Нужно передать хотя бы одно поле для изменения")

    unknown_fields = set(data) - allowed_fields
    if unknown_fields:
        raise ValidationError(f"Недопустимые поля: {', '.join(sorted(unknown_fields))}")

    for key, value in data.items():
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"Поле '{key}' должно быть непустой строкой")
