
async def test_show_articles(client):
    resp = await client.get('/article/1')
    assert resp.status == 200
