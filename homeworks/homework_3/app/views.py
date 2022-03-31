from aiohttp import web
import aiohttp_jinja2

from app.exceptions import MissingFieldException
from app.utils import get_url_location, get_created_at_time, get_current_page

ARTICLES = [{'name': 'Article 1', 'body': 'Article 1 body', 'tags': 'Tag1, tag2',
             'created_at': get_created_at_time()},
            {'name': 'Article 2', 'body': 'Article 2 body', 'tags': 'Tag1, tag2',
             'created_at': get_created_at_time()}]


async def health(request: web.Request) -> web.Response:
    return web.Response(text='We are ready to serve you!')


async def redirect_article(request: web.Request) -> web.Response:
    location = get_url_location(request, 'articles', '1')
    return web.HTTPFound(location=location)


async def articles(request: web.Request) -> web.Response:
    page = int(request.match_info['page'])
    unit = len(ARTICLES) // 5
    is_next_page = False
    if page > (unit + 1):
        articles_ = []
    else:
        slice_ = page - 1
        slice_ *= 5
        articles_ = ARTICLES[::-1][slice_:slice_ + 5]
        if len(articles_) == 5:
            is_next_page = True

    context = {'articles': articles_,
               'page': page,
               'is_next_page': True if is_next_page else False,
               'is_previous_page': page != 1,
               'previous_page_url': get_url_location(request, 'articles', str(page - 1)),
               'next_page_url': get_url_location(request, 'articles', str(page + 1)),
               'redirect_url': get_url_location(request, 'create-article-get')}
    return aiohttp_jinja2.render_template('index.html', request, context=context)


async def create_article(request: web.Request) -> web.Response:
    if request.method == 'POST':
        data = await request.post()
        if not all(data.values()):
            missing_field = ', '.join([key for key in data if not data[key]])
            raise MissingFieldException(text=f"Not all fields are filled correctly: {missing_field}")
        article = {**data}
        article.update({'created_at': get_created_at_time()})
        ARTICLES.append(article)
        current_page = get_current_page(ARTICLES)
        location = get_url_location(request, 'articles', current_page)
        raise web.HTTPFound(location=location)

    elif request.method == 'GET':
        context = {'redirect_url': get_url_location(request, 'create-article-post')}
        return aiohttp_jinja2.render_template('article.html', request, context=context)
