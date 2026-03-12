from aiohttp import web

from app.auth import (
    AuthError,
    BadRequestError,
    ConflictError,
    NotFoundError,
    PermissionDenied,
    ValidationError,
)


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        response = await handler(request)
        if response.status == 404:
            return web.json_response({"error": "Маршрут не найден"}, status=404)
        return response
    except ValidationError as exc:
        return web.json_response({"error": str(exc)}, status=400)
    except BadRequestError as exc:
        return web.json_response({"error": str(exc)}, status=400)
    except AuthError as exc:
        return web.json_response({"error": str(exc)}, status=401)
    except PermissionDenied as exc:
        return web.json_response({"error": str(exc)}, status=403)
    except NotFoundError as exc:
        return web.json_response({"error": str(exc)}, status=404)
    except ConflictError as exc:
        return web.json_response({"error": str(exc)}, status=409)
    except web.HTTPException as exc:
        return web.json_response({"error": exc.reason}, status=exc.status)
    except Exception:
        return web.json_response({"error": "Внутренняя ошибка сервера"}, status=500)
