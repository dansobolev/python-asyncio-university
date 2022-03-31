from aiohttp import web

from app.db import db, init_db, close_db


async def cleanup_ctx(app: web.Application):

    await init_db(app, db)
    yield
    await close_db(db)
