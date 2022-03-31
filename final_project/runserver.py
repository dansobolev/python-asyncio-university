from aiohttp import web

from app import aiohttp_app
from app.config import Config


web.run_app(aiohttp_app(),
            host=Config.AIO_HOST,
            port=Config.AIO_PORT)
