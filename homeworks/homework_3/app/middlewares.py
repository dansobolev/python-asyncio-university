from typing import Dict, Callable

import aiohttp_jinja2
from aiohttp import web

from app.utils import get_url_location


async def handle_400(request: web.Request, context: Dict = None):
    context.update({'redirect_url': get_url_location(request, 'create-article-get')})
    return aiohttp_jinja2.render_template('exceptions/400.html', request, context=context, status=400)


async def handle_404(request: web.Request, context: Dict = None):
    return aiohttp_jinja2.render_template('exceptions/404.html', request, context=context, status=404)


async def handle_500(request: web.Request, context: Dict = None):
    return aiohttp_jinja2.render_template('exceptions/500.html', request, context=context, status=500)


def create_error_middleware(overrides: Dict[int, Callable]):

    @web.middleware
    async def error_middleware(request: web.Request, handler: Callable):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request, {'error_message': ex.text})
            raise
        except Exception:
            request.protocol.logger.exception("Error handling request")
            return await overrides[500](request)

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        400: handle_400,
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
