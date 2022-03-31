from aiohttp import web

from app.config import Config
from app.views.users import routes as user_routes
from app.views.discussions import routes as post_routes
from app.views.uploads import routes as upload_routes


def setup_routes(app: web.Application):
    app.add_routes([
        web.static('/static', Config.UPLOAD_FOLDER_PATH),
        *user_routes, *post_routes, *upload_routes
    ])
