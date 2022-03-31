import pytest
from app import aiohttp_app
from app.utils import get_created_at_time


@pytest.fixture
def client(event_loop, aiohttp_client):
    app = aiohttp_app()
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def articles():
    return [{'name': 'Article 1', 'body': 'Article 1 body', 'tags': 'Tag1, tag2',
             'created_at': get_created_at_time()},
            {'name': 'Article 2', 'body': 'Article 2 body', 'tags': 'Tag1, tag2',
             'created_at': get_created_at_time()},
            {'name': 'Article 3', 'body': 'Article 3 body', 'tags': 'Tag1, tag2',
             'created_at': get_created_at_time()}]
