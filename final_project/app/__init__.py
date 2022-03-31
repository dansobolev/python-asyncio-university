"""
Project description
"""

from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
import aiohttp_jinja2
from cryptography import fernet
import jinja2

from app.routes import setup_routes
from app.middlewares import setup_middlewares
from app.config import Config
from app.context import cleanup_ctx
from app.auth.authorization import AuthorizationPolicy


def create_app() -> web.Application:
    app = web.Application()
    app['config'] = Config

    setup_routes(app)
    # TODO: uncomment
    # setup_middlewares(app)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(Config.BASE_DIR) + '/templates'))

    app.cleanup_ctx.append(cleanup_ctx)

    cookie_secret = fernet.Fernet.generate_key()
    f = fernet.Fernet(cookie_secret)
    setup_session(app, EncryptedCookieStorage(f))

    policy = SessionIdentityPolicy()
    setup_security(app, policy, AuthorizationPolicy())

    return app


aiohttp_app = create_app
