from typing import List, Dict

from datetime import datetime
from aiohttp import web

from app.config import Config


def get_url_location(request: web.Request, url_name: str, page_: str = None) -> str:
    if page_:
        url = request.app.router[url_name].url_for(page=page_)
    else:
        url = request.app.router[url_name].url_for()
    return Config.BASE_URL + str(url)


def get_created_at_time() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def get_current_page(articles: List[Dict]) -> str:
    page = len(articles) // 5
    if page == 0 or page == 1:
        return '1'
    return str(page)
