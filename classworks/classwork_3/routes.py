from aiohttp import web

from views import health, input_name


def setup_routes(app):
    # TODO: change add routes through decorators for each handler
    app.add_routes([web.get('/health', health)])
    app.add_routes([web.get('/input-name', input_name)])
    app.add_routes([web.post('/input-name', input_name, name='input-name')])
