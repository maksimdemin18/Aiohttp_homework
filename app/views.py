from aiohttp import web
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth import (
    ConflictError,
    NotFoundError,
    PermissionDenied,
    generate_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.models import Advertisement, User
from app.validators import (
    get_json,
    require_fields,
    validate_ad_update_data,
    validate_email,
    validate_password,
)

routes = web.RouteTableDef()


@routes.get("/health")
async def health_check(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})


@routes.post("/users")
async def create_user(request: web.Request) -> web.Response:
    data = await get_json(request)
    require_fields(data, ["email", "password"])
    email = data["email"].strip().lower()
    password = data["password"].strip()

    validate_email(email)
    validate_password(password)

    async with request.app["db_sessionmaker"]() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        if existing_user is not None:
            raise ConflictError("Пользователь с таким email уже существует")

        user = User(email=email, password_hash=hash_password(password))
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return web.json_response(
        {"id": user.id, "email": user.email, "message": "Пользователь создан"},
        status=201,
    )


@routes.post("/login")
async def login(request: web.Request) -> web.Response:
    data = await get_json(request)
    require_fields(data, ["email", "password"])
    email = data["email"].strip().lower()
    password = data["password"].strip()

    async with request.app["db_sessionmaker"]() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user is None or not verify_password(password, user.password_hash):
            return web.json_response({"error": "Неверный email или пароль"}, status=401)

        user.token = generate_token()
        await session.commit()
        await session.refresh(user)

    return web.json_response({"token": user.token})


@routes.post("/ads")
async def create_ad(request: web.Request) -> web.Response:
    current_user = await get_current_user(request)
    data = await get_json(request)
    require_fields(data, ["title", "description"])

    async with request.app["db_sessionmaker"]() as session:
        ad = Advertisement(
            title=data["title"].strip(),
            description=data["description"].strip(),
            owner_id=current_user.id,
        )
        session.add(ad)
        await session.commit()
        await session.refresh(ad)

    return web.json_response(
        {
            "id": ad.id,
            "title": ad.title,
            "description": ad.description,
            "created_at": ad.created_at.isoformat(),
            "owner_id": ad.owner_id,
        },
        status=201,
    )


@routes.get("/ads/{ad_id:\\d+}")
async def get_ad(request: web.Request) -> web.Response:
    ad_id = int(request.match_info["ad_id"])

    async with request.app["db_sessionmaker"]() as session:
        result = await session.execute(
            select(Advertisement)
            .options(selectinload(Advertisement.owner))
            .where(Advertisement.id == ad_id)
        )
        ad = result.scalar_one_or_none()
        if ad is None:
            raise NotFoundError("Объявление не найдено")

    return web.json_response(
        {
            "id": ad.id,
            "title": ad.title,
            "description": ad.description,
            "created_at": ad.created_at.isoformat(),
            "owner": {"id": ad.owner.id, "email": ad.owner.email},
        }
    )


@routes.patch("/ads/{ad_id:\\d+}")
async def update_ad(request: web.Request) -> web.Response:
    current_user = await get_current_user(request)
    ad_id = int(request.match_info["ad_id"])
    data = await get_json(request)
    validate_ad_update_data(data)

    async with request.app["db_sessionmaker"]() as session:
        result = await session.execute(select(Advertisement).where(Advertisement.id == ad_id))
        ad = result.scalar_one_or_none()
        if ad is None:
            raise NotFoundError("Объявление не найдено")
        if ad.owner_id != current_user.id:
            raise PermissionDenied("Редактировать объявление может только владелец")

        if "title" in data:
            ad.title = data["title"].strip()
        if "description" in data:
            ad.description = data["description"].strip()

        await session.commit()
        await session.refresh(ad)

    return web.json_response(
        {
            "id": ad.id,
            "title": ad.title,
            "description": ad.description,
            "created_at": ad.created_at.isoformat(),
            "owner_id": ad.owner_id,
            "message": "Объявление обновлено",
        }
    )


@routes.delete("/ads/{ad_id:\\d+}")
async def delete_ad(request: web.Request) -> web.Response:
    current_user = await get_current_user(request)
    ad_id = int(request.match_info["ad_id"])

    async with request.app["db_sessionmaker"]() as session:
        result = await session.execute(select(Advertisement).where(Advertisement.id == ad_id))
        ad = result.scalar_one_or_none()
        if ad is None:
            raise NotFoundError("Объявление не найдено")
        if ad.owner_id != current_user.id:
            raise PermissionDenied("Удалять объявление может только владелец")

        await session.delete(ad)
        await session.commit()

    return web.json_response({"status": "deleted"})
