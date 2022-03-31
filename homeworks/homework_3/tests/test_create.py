from copy import deepcopy
import pytest

from app.views import ARTICLES


async def test_health_server(client):
    resp = await client.get('/health')
    assert resp.status == 200
    assert await resp.text() == 'We are ready to serve you!'


async def test_create_article(client):
    data = {'name': 'test_article',
            'body': 'body for test article',
            'tags': 'test tags for test article'}
    article_before = deepcopy(ARTICLES)
    with pytest.raises(Exception) as e:
        await client.post('/create-article', data=data)

    assert len(article_before) == len(ARTICLES) - 1
    new_article = ARTICLES[-1]
    del new_article['created_at']
    assert new_article == data


empty_data = (
    {'name': 'Article wrong test', 'body': '', 'tags': ''},
    {'name': '', 'body': 'Article only with body', 'tags': ''},
    {'name': '', 'body': '', 'tags': 'Article only with tags'}
)


@pytest.mark.parametrize("data", empty_data)
async def test_create_article_with_empty_fields(client, data):
    resp = await client.post('/create-article', data=data)
    assert resp.status == 400
