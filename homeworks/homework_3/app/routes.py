from aiohttp import web

from app.views import health, articles, create_article, redirect_article


def setup_routes(app):
    app.add_routes([web.get('/health', health)])
    app.add_routes([web.get('/', redirect_article, name='redirect-article')])
    app.add_routes([web.get('/article/{page}', articles, name='articles')])
    app.add_routes([web.get('/create-article', create_article, name='create-article-get')])
    app.add_routes([web.post('/create-article', create_article, name='create-article-post')])
