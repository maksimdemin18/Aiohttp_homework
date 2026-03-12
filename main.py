from aiohttp import web

from app.config import HOST, PORT
from app.db import SessionLocal, close_db, init_db
from app.middleware import error_middleware
from app.views import routes


async def on_startup(app: web.Application) -> None:
    await init_db()


async def on_cleanup(app: web.Application) -> None:
    await close_db()



def create_app() -> web.Application:
    app = web.Application(middlewares=[error_middleware])
    app["db_sessionmaker"] = SessionLocal
    app.add_routes(routes)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host=HOST, port=PORT)
