from aiohttp import web
from app import aiohttp_app

web.run_app(aiohttp_app())
